<template>
  <h2>Comments</h2>
  <CommentForm />
  <hr />
  <CommentList />
</template>

<script setup>
import CommentForm from "./components/CommentForm.vue";
import CommentList from "./components/CommentList.vue";
</script>

<style>
body{font-family:system-ui,Arial,sans-serif;margin:20px}
</style>
