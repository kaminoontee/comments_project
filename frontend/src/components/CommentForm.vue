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
  parentId: { type: Number, default: null } // ID родителя (для ответов)
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
    form.append("parent", props.parentId);
  }
  if (file.value) {
    form.append("file", file.value);
  }

  try {
    await api.post("comments/", form);
    emit("submitted");

    // 🔹 Полная очистка формы
    username.value = "";
    email.value = "";
    homepage.value = "";
    text.value = "";
    file.value = null;
    captchaAnswer.value = "";

    if (fileInput.value) fileInput.value.value = "";

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
  gap: 12px;
}

.form input,
.form textarea,
.form select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #b5d6f5;
  border-radius: 8px;
  font-size: 14px;
  background: #eaf4fb;   /* голубой фон */
  color: #000;           /* текст чёрный */
  transition: border 0.2s, box-shadow 0.2s, background 0.2s;
}

.form input::placeholder,
.form textarea::placeholder {
  color: #333; /* placeholder тоже тёмный */
}

.form input:focus,
.form textarea:focus {
  border-color: #4a90e2;
  background: #fff; /* при фокусе фон белый */
  outline: none;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.captcha-box {
  display: flex;
  align-items: center;
  gap: 10px;
}

.captcha-box img {
  border: 1px solid #ddd;
  border-radius: 6px;
  height: 50px;
}

.actions {
  margin-top: 8px;
}

.btn {
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

.btn.primary {
  background: #4a90e2;
  color: white;
}

.btn.primary:hover {
  background: #357abd;
}

.btn.secondary {
  background: #eee;
  color: #333;
}

.btn.secondary:hover {
  background: #ddd;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 500px;
  margin: 0 auto;
}

.form input,
.form textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #eaf7ff; /* светло-голубой */
  color: #000; /* чёрный текст */
  font-size: 14px;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

/* Блок капчи */
.captcha-block {
  display: flex;
  align-items: center;
  gap: 10px;
}

.captcha-block img {
  height: 40px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.captcha-input {
  flex: 1;
}

/* Кнопки */
.actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

button {
  background: #27c7b8;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

button:hover {
  background: #1fa699;
}

button:active {
  transform: scale(0.96);
}
</style>
