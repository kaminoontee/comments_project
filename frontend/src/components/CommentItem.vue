<template>
  <div class="comment">
    <!-- аватар -->
    <div class="avatar">
      <img
        :src="avatarUrl(c.user?.username)"
        alt="avatar"
      />
    </div>

    <!-- тело комментария -->
    <div class="body">
      <div class="meta">
        <strong class="username">{{ c.user?.username || "Anonym" }}</strong>
        <span class="date">{{ new Date(c.created_at).toLocaleString() }}</span>
      </div>

      <div class="text" v-html="c.text"></div>

      <!-- прикреплённый файл -->
      <div v-if="c.file" class="attachment">
        <img v-if="isImage(c.file)" :src="c.file" alt="attachment" />
        <a v-else :href="c.file" target="_blank" rel="noopener noreferrer">
          📄 Открыть файл
        </a>
      </div>

      <!-- кнопки -->
      <div class="actions">
        <button @click="replying = !replying">
          {{ replying ? "Отмена" : "Ответить" }}
        </button>
      </div>

      <!-- форма ответа -->
      <CommentForm
        v-if="replying"
        :parent-id="c.id"
        @submitted="onReply"
      />

      <!-- рекурсивные ответы -->
      <div class="replies" v-if="c.replies?.length">
        <CommentItem v-for="r in c.replies" :key="r.id" :c="r" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import CommentForm from "./CommentForm.vue";
import CommentItem from "./CommentItem.vue";

const props = defineProps({ c: Object });
const replying = ref(false);

const isImage = (url) => /\.(jpg|jpeg|png|gif)$/i.test(url);

const avatarUrl = (username) => {
  // простая заглушка: генерируем аватар через https://ui-avatars.com/
  return `https://ui-avatars.com/api/?name=${username || "A"}&background=random`;
};

const onReply = () => {
  replying.value = false;
};
</script>

<style scoped>
.comment {
  display: flex;
  gap: 12px;
  padding: 15px;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  margin: 12px 0;
  background: #fafafa;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #ddd;
}

.body {
  flex: 1;
}

.meta {
  font-size: 14px;
  color: #666;
  margin-bottom: 6px;
}

.username {
  font-weight: bold;
  color: #222;
  margin-right: 8px;
}

.date {
  font-size: 12px;
  color: #888;
}

.text {
  font-size: 15px;
  margin-bottom: 6px;
  line-height: 1.5;
}

.attachment {
  margin: 6px 0;
}
.attachment img {
  max-width: 220px;
  max-height: 160px;
  border-radius: 6px;
  border: 1px solid #ddd;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.actions {
  margin-top: 8px;
}
.actions button {
  font-size: 13px;
  color: #4a90e2;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}
.actions button:hover {
  text-decoration: underline;
}

.replies {
  margin-top: 12px;
  margin-left: 50px;
  border-left: 2px solid #f0f0f0;
  padding-left: 12px;
}
</style>

