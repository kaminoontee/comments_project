<template>
  <div class="item">
    <div class="meta">
      <strong>{{ c.user?.username }}</strong>
      <small> · {{ new Date(c.created_at).toLocaleString() }}</small>
    </div>

    <div class="text" v-html="c.text"></div>

    <!-- вложенный файл -->
    <div v-if="c.file" class="attachment">
      <img
        v-if="isImage(c.file)"
        :src="c.file"
        alt="attachment"
      />
      <pre v-else-if="isText(c.file)" class="txt-preview">{{ txtContent }}</pre>
      <a
        v-else
        :href="c.file"
        target="_blank"
        rel="noopener noreferrer"
      >
        📎 Open file
      </a>
    </div>

    <!-- рекурсивные ответы -->
    <div class="replies" v-if="c.replies?.length">
      <CommentItem v-for="r in c.replies" :key="r.id" :c="r" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import CommentItem from "./CommentItem.vue";

const props = defineProps({ c: Object });

const txtContent = ref("");

// утилиты
const isImage = (url) => /\.(jpg|jpeg|png|gif)$/i.test(url);
const isText = (url) => /\.txt$/i.test(url);

// если файл текстовый → грузим его содержимое
watch(
  () => props.c?.file,
  async (newFile) => {
    if (newFile && isText(newFile)) {
      try {
        const res = await fetch(newFile);
        txtContent.value = await res.text();
      } catch (err) {
        txtContent.value = "⚠️ Не удалось загрузить текстовый файл.";
      }
    }
  },
  { immediate: true }
);
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
.txt-preview {
  margin-top: 6px;
  padding: 6px;
  background: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 4px;
  white-space: pre-wrap;
  max-width: 600px;
  max-height: 200px;
  overflow: auto;
}
.replies {
  margin-left: 8px;
}
</style>
