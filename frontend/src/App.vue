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
body {
  margin: 0;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background: #fff; /* 👈 вся страница белая */
  color: #222;
}

button,
.btn {
  display: inline-block;
  background: #27c7b8;  /* бирюзовый */
  color: #fff;          /* белый текст */
  border: none;
  padding: 8px 16px;
  border-radius: 20px;  /* закруглённые */
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

button:hover,
.btn:hover {
  background: #1fa699;  /* чуть темнее при наведении */
}

button:active,
.btn:active {
  transform: scale(0.96);  /* небольшой клик-эффект */
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

h1 {
  text-align: center;
  margin-bottom: 8px;
}

.subtitle {
  text-align: center;
  color: #555;
  margin-bottom: 24px;
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

.form-section h2,
.comments-section h2 {
  margin-top: 0;
  font-size: 18px;
}
</style>

