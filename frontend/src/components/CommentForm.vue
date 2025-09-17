<template>
  <form @submit.prevent="submitComment" class="form">
    <input v-model="username" placeholder="username" required />
    <input v-model="email" type="email" placeholder="email" required />
    <input v-model="homepage" type="url" placeholder="homepage (optional)" />

    <textarea v-model="text" rows="4" placeholder="your comment..." required></textarea>

    <!-- file upload -->
    <input type="file" ref="fileInput" @change="onFile" />

    <!-- captcha -->
    <div v-if="captcha" class="captcha-container">
      <div class="captcha-box">
        <img :src="captcha.image_url" alt="captcha" />
        <input
          v-model="captchaAnswer"
          placeholder="enter captcha"
          required
          :class="{ shake: isCaptchaError }"
          @animationend="isCaptchaError = false"
        />
        <button
          type="button"
          @click="fetchCaptcha"
          :class="{ 'refresh-error': isCaptchaError }"
        >
          refresh
        </button>
      </div>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
    <div v-else>
      <p>Loading captcha...</p>
    </div>

    <div class="actions">
      <button type="submit">send</button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "../services/api";

const props = defineProps({
  parentId: { type: Number, default: null }
});
const emit = defineEmits(["submitted"]);

const username = ref("");
const email = ref("");
const homepage = ref("");
const text = ref("");
const file = ref(null);
const captcha = ref(null);
const captchaAnswer = ref("");
const errorMessage = ref("");
const isCaptchaError = ref(false);

const fileInput = ref(null);

const fetchCaptcha = async () => {
  const { data } = await api.get("captcha/");
  captcha.value = data;
  errorMessage.value = "";
};

// при монтировании подтягиваем капчу + данные пользователя
onMounted(() => {
  fetchCaptcha();

  const savedUsername = localStorage.getItem("username");
  const savedEmail = localStorage.getItem("email");

  if (savedUsername) username.value = savedUsername;
  if (savedEmail) email.value = savedEmail;
});

const onFile = (e) => {
  file.value = e.target.files[0];
};

const submitComment = async () => {
  if (!captcha.value) {
    errorMessage.value = "Captcha not loaded yet";
    return;
  }

  const form = new FormData();
  form.append("username", username.value);
  form.append("email", email.value);
  form.append("homepage", homepage.value);
  form.append("text", text.value);
  form.append("captcha_id", captcha.value.id);
  form.append("captcha_answer", captchaAnswer.value);

  if (props.parentId) form.append("parent", props.parentId);
  if (file.value) form.append("file", file.value);

  try {
    await api.post("comments/", form);
    emit("submitted");

    // очищаем только текст и файл, а username/email остаются
    text.value = "";
    file.value = null;
    captchaAnswer.value = "";
    if (fileInput.value) fileInput.value.value = "";

    errorMessage.value = "";
    await fetchCaptcha();
  } catch (err) {
    console.error(err.response?.data || err.message);

    if (err.response?.data?.captcha) {
      isCaptchaError.value = true;
    } else {
      errorMessage.value = "Error while submitting the comment";
    }

    await fetchCaptcha();
  }
};
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 500px;
  margin: 0 auto;
}

.form input,
.form textarea,
.form select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #b5d6f5;
  border-radius: 8px;
  font-size: 14px;
  background: #eaf4fb;
  color: #000;
  transition: border 0.2s, box-shadow 0.2s, background 0.2s;
}

.form input::placeholder,
.form textarea::placeholder {
  color: #333;
}

.form input:focus,
.form textarea:focus {
  border-color: #4a90e2;
  background: #fff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

/* FIXED textarea size */
textarea {
  resize: none;
  height: 120px;
  min-height: 120px;
  max-height: 120px;
}

/* Captcha container */
.captcha-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

/* Captcha row */
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

.captcha-box input {
  width: 120px;
  padding: 8px;
  border: 1px solid #b5d6f5;
  border-radius: 6px;
  font-size: 14px;
  background: #eaf4fb;
  color: #000;
}

/* Error message */
.error {
  color: red;
  font-size: 13px;
  text-align: center;
}

/* Shake animation */
.shake {
  animation: shake 0.3s ease-in-out 2;
}
@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  50% { transform: translateX(5px); }
  75% { transform: translateX(-5px); }
  100% { transform: translateX(0); }
}

/* Buttons */
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

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Refresh button error animation */
.refresh-error {
  animation: flash-red 1s ease-in-out 2;
}
@keyframes flash-red {
  0%, 100% { background: #27c7b8; }
  50% { background: #e74c3c; }
}

/* SEND button style */
.actions button {
  background: #455a64;
  color: #fff;
  border: none;
  padding: 14px 14px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  min-width: 120px;
  text-align: center;
}

.actions button:hover {
  background: #37474f;
}

.actions button:active {
  transform: scale(0.97);
}

.actions button:disabled {
  background: #9e9e9e;
  cursor: not-allowed;
}

</style>
