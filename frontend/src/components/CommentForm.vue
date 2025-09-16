<template>
  <form @submit.prevent="submitComment" class="form">
    <input v-model="username" placeholder="Username" required />
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="homepage" type="url" placeholder="Homepage (optional)" />

    <div class="toolbar">
      <button type="button" @click="wrap('i')">[i]</button>
      <button type="button" @click="wrap('strong')">[strong]</button>
      <button type="button" @click="wrap('code')">[code]</button>
      <button type="button" @click="wrapLink">[a]</button>
    </div>

    <textarea ref="ta" v-model="text" rows="6" placeholder="Your comment..." required></textarea>

    <input type="file" @change="onFile" />

    <div v-if="captcha">
        <img :src="captcha.image_url" alt="captcha" />
        <input v-model="captchaAnswer" placeholder="Enter captcha" required />
        <button type="button" @click="fetchCaptcha">Refresh</button>
    </div>
    <div v-else>
      <p>Loading captcha...</p>
    </div>

    <div class="actions">
      <button type="button" @click="preview">Preview</button>
      <button type="submit">Send</button>
    </div>

    <div v-if="previewHtml" class="preview" v-html="previewHtml"></div>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "../services/api";

const username = ref("");
const email = ref("");
const homepage = ref("");
const text = ref("");
const file = ref(null);
const captcha = ref(null);
const captchaAnswer = ref("");
const previewHtml = ref("");
const ta = ref(null);

const fetchCaptcha = async () => {
  const { data } = await api.get("captcha/");
  captcha.value = data; // {id, image_url}
};
onMounted(fetchCaptcha);

const onFile = (e) => {
  file.value = e.target.files[0];
};

const wrap = (tag) => {
  const el = ta.value;
  const start = el.selectionStart, end = el.selectionEnd;
  const sel = text.value.slice(start, end) || "text";
  const before = text.value.slice(0, start);
  const after  = text.value.slice(end);
  text.value = `${before}<${tag}>${sel}</${tag}>${after}`;
  el.focus();
};

const wrapLink = () => {
  const url = prompt("Enter URL (http/https):", "https://");
  if (!url) return;
  const el = ta.value;
  const start = el.selectionStart, end = el.selectionEnd;
  const sel = text.value.slice(start, end) || "link";
  const before = text.value.slice(0, start);
  const after  = text.value.slice(end);
  text.value = `${before}<a href="${url}">${sel}</a>${after}`;
  el.focus();
};

const preview = async () => {
  try {
    const { data } = await api.post("preview/", { text: text.value });
    previewHtml.value = data.html;
  } catch (err) {
    console.error("Preview error:", err);
  }
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
  if (file.value) form.append("file", file.value);

  try {
    await api.post("comments/", form);
    alert("Comment added!");
    // очистка формы
    text.value = "";
    file.value = null;
    captchaAnswer.value = "";
    previewHtml.value = "";
    await fetchCaptcha();
  } catch (err) {
    console.error("Submit error:", err.response?.data || err.message);
    alert("Error: " + JSON.stringify(err.response?.data || err.message));
  }
};
</script>

<style scoped>
.form{display:grid;gap:10px;max-width:720px}
.toolbar{display:flex;gap:6px}
.actions{display:flex;gap:8px}
.preview{margin-top:8px;padding:10px;border:1px solid #eee;border-radius:8px;background:#fafafa}
</style>
