<template>
  <div class="item">
    <div class="meta">
      <strong>{{ c.user?.username }}</strong>
      <small> · {{ new Date(c.created_at).toLocaleString() }}</small>
    </div>
    <div class="text" v-html="c.text"></div>
    <div class="replies" v-if="c.replies?.length">
      <CommentItem v-for="r in c.replies" :key="r.id" :c="r"/>
    </div>
  </div>
</template>

<script setup>
import CommentItem from "./CommentItem.vue";
defineProps({ c: Object });
</script>

<style scoped>
.item{margin:12px 0;padding-left:8px;border-left:2px solid #eee}
.meta{margin-bottom:4px}
.text{white-space:pre-wrap}
.replies{margin-left:8px}
</style>
