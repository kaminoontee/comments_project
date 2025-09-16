<template>
  <div class="app">
    <div class="container">
      <!-- секция формы -->
      <div class="form-section">
        <h2>leave a comment</h2>
        <CommentForm @submitted="refreshComments" />
      </div>

      <!-- секция списка -->
      <div class="comments-section">
        <h2>comments</h2>
        <CommentList ref="commentList" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import CommentForm from "./components/CommentForm.vue";
import CommentList from "./components/CommentList.vue";

const commentList = ref(null);

const refreshComments = () => {
  commentList.value?.load(); // обновляем список после отправки формы
};
</script>

<style>
body {
  margin: 0;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background: #fff;
  color: #222;
}

button,
.btn {
  display: inline-block;
  background: #27c7b8;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

button:hover,
.btn:hover {
  background: #1fa699;
}

button:active,
.btn:active {
  transform: scale(0.96);
}

button:disabled,
.btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.app {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

.container {
  width: 100%;
  max-width: 800px;
}

.form-section,
.comments-section {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

h2 {
  margin-top: 0;
  font-size: 18px;
  margin-bottom: 16px;
}
</style>
