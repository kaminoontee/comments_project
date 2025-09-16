<template>
  <div class="controls">
    <label>Sort by:
      <select v-model="ordering" @change="load">
        <option value="-created_at">Newest</option>
        <option value="created_at">Oldest</option>
        <option value="user__username">Username</option>
        <option value="user__email">Email</option>
      </select>
    </label>
  </div>

  <CommentItem
  v-for="c in results"
  :key="c.id"
  :c="c"
  @submitted="load"
/>

  <div class="pager">
    <button :disabled="!prev" @click="go(prev)">Prev</button>
    <button :disabled="!next" @click="go(next)">Next</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "../services/api";
import CommentItem from "./CommentItem.vue";

const results = ref([]);
const next = ref(null);
const prev = ref(null);
const ordering = ref("-created_at");

const buildUrl = (pageUrl = null) => {
  if (pageUrl) return pageUrl; // уже полная ссылка от DRF
  return `comments/?ordering=${encodeURIComponent(ordering.value)}`;
};

const load = async (pageUrl = null) => {
  const { data } = await api.get(buildUrl(pageUrl));
  results.value = data.results ?? data; // DRF пагинация вернёт results/next/previous
  next.value = data.next;
  prev.value = data.previous;
};

const go = async (url) => load(url);

onMounted(load);

// 👇 добавляем это, чтобы App.vue мог вызвать commentList.value.load()
defineExpose({ load });
</script>

<style scoped>
.controls {
  margin-bottom: 10px;
}
.pager {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}
</style>
