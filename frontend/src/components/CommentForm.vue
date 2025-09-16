<template>
  <form @submit.prevent="submitComment" class="form">
    <input v-model="username" placeholder="Username" required />
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="homepage" type="url" placeholder="Homepage (optional)" />

    <textarea v-model="text" rows="4" placeholder="Your comment..." required></textarea>

    <!-- выбор файла -->
    <input type="file" ref="fileInput" @change="onFile" />

    <!-- капча -->
    <div v-if="captcha">
      <img :src="captcha.image_url" alt="captcha" />
      <input v-model="captchaAnswer" placeholder="Enter captcha" required />
      <button type="button" @click="fetchCaptcha">Refresh</button>
    </div>
    <div v-else>
      <p>Loading captcha...</p>
    </div>

    <div class="actions">
      <button type="submit">Send</button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "../services/api";

const props = defineProps({
  parentId: { type: Number, default: null } // 👈 ID родителя (для ответов)
});
const emit = defineEmits(["submitted"]); // событие после отправки

const username = ref("");
const email = ref("");
const homepage = ref("");
const text = ref("");
const file = ref(null);
const captcha = ref(null);
const captchaAnswer = ref("");

// ref для очистки input type="file"
const fileInput = ref(null);

const fetchCaptcha = async () => {
  const { data } = await api.get("captcha/");
  captcha.value = data;
};
onMounted(fetchCaptcha);

const onFile = (e) => {
  file.value = e.target.files[0];
};

const submitComment = async () => {
  if (!captcha.value) {
    alert("Captcha not loaded yet");
    return;
  }

  const form = new FormData();
  form.append("username", username.value);
  form.append("email", email.value);
  form.append("homepage", homepage.value);
  form.append("text", text.value);
  form.append("captcha_id", captcha.value.id);
  form.append("captcha_answer", captchaAnswer.value);

  if (props.parentId) {
    form.append("parent", props.parentId); // 👈 если это ответ
  }
  if (file.value) {
    form.append("file", file.value);
  }

  console.log("Submitting:", [...form.entries()]); // 👈 дебаг

  try {
    await api.post("comments/", form);
    emit("submitted");

    // очистка формы
    text.value = "";
    file.value = null;
    captchaAnswer.value = "";
    if (fileInput.value) fileInput.value.value = ""; // 👈 очищаем инпут файла
    await fetchCaptcha();
  } catch (err) {
    console.error(err.response?.data || err.message);
    alert("Error: " + JSON.stringify(err.response?.data || err.message));
  }
};
</script>

<style scoped>
.form {
  display: grid;
  gap: 10px;
  max-width: 500px;
  margin: 10px 0;
}
.actions {
  margin-top: 8px;
}
</style>
