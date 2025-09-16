<template>
  <div class="item">
    <div class="meta">
      <strong>{{ c.user?.username }}</strong>
      <small> · {{ new Date(c.created_at).toLocaleString() }}</small>
    </div>

    <div class="text" v-html="c.text"></div>

    <!-- прикреплённый файл -->
    <div v-if="c.file" class="attachment">
      <img v-if="isImage(c.file)" :src="c.file" alt="attachment" />
      <a v-else :href="c.file" target="_blank" rel="noopener noreferrer">
        📄 Preview file
      </a>
    </div>

    <!-- кнопка ответа -->
    <div class="actions">
      <button @click="replying = !replying">
        {{ replying ? "Cancel" : "Reply" }}
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
</template>

<script setup>
import { ref } from "vue";
import CommentForm from "./CommentForm.vue";
import CommentItem from "./CommentItem.vue";

const props = defineProps({ c: Object });
const replying = ref(false);

const isImage = (url) => /\.(jpg|jpeg|png|gif)$/i.test(url);

const onReply = () => {
  replying.value = false; // закрываем форму после отправки
};
</script>

<style scoped>
.item {
  margin: 12px 0;
  padding-left: 8px;
  border-left: 2px solid #eee;
}
.meta {
  margin-bottom: 4px;
}
.text {
  white-space: pre-wrap;
}
.attachment {
  margin-top: 6px;
}
.attachment img {
  max-width: 320px;
  max-height: 240px;
  display: block;
  margin-top: 4px;
  border-radius: 4px;
  border: 1px solid #ddd;
}
.actions {
  margin-top: 6px;
}
.replies {
  margin-left: 12px;
  margin-top: 8px;
}
</style>
