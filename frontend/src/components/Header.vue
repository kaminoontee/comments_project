<template>
  <header class="header">
    <div class="logo">mini-forum</div>

    <nav class="auth-buttons">
      <template v-if="!isLoggedIn">
        <button @click="showLogin = true">Log in</button>
        <button @click="showRegister = true">Sign up</button>
      </template>
      <template v-else>
        <span class="welcome">Hello, {{ username }}</span>
        <button @click="handleLogout">Logout</button>
      </template>
    </nav>

    <!-- Login Modal -->
    <div v-if="showLogin" class="modal">
      <div class="modal-content">
        <h3>log in</h3>
        <input v-model="loginUsername" placeholder="Username" />
        <input v-model="loginPassword" type="password" placeholder="Password" />
        <div class="actions">
          <button @click="handleLogin">Log in</button>
          <button class="secondary" @click="showLogin = false">Cancel</button>
        </div>
        <p v-if="loginError" class="error">{{ loginError }}</p>
      </div>
    </div>

    <!-- Register Modal -->
    <div v-if="showRegister" class="modal">
      <div class="modal-content">
        <h3>sign up</h3>
        <input v-model="registerUsername" placeholder="Username" />
        <input v-model="registerEmail" type="email" placeholder="Email" />
        <input v-model="registerPassword" type="password" placeholder="Password" />
        <div class="actions">
          <button @click="handleRegister">Sign up</button>
          <button class="secondary" @click="showRegister = false">Cancel</button>
        </div>
        <p v-if="registerError" class="error">{{ registerError }}</p>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { login, register, logout, isAuthenticated } from "../services/api";

const isLoggedIn = ref(false);
const username = ref("");

// modal states
const showLogin = ref(false);
const showRegister = ref(false);

// login form
const loginUsername = ref("");
const loginPassword = ref("");
const loginError = ref("");

// register form
const registerUsername = ref("");
const registerEmail = ref("");
const registerPassword = ref("");
const registerError = ref("");

// check if already logged in
onMounted(() => {
  isLoggedIn.value = isAuthenticated();
  if (isLoggedIn.value) {
    username.value = localStorage.getItem("username") || "User";
  }
});

const handleLogin = async () => {
  try {
    await login(loginUsername.value, loginPassword.value);
    isLoggedIn.value = true;
    username.value = loginUsername.value;
    localStorage.setItem("username", loginUsername.value);
    showLogin.value = false;
    loginError.value = "";
  } catch (err) {
    console.error(err);
    loginError.value = "Invalid username or password";
  }
};

const handleRegister = async () => {
  try {
    await register(registerUsername.value, registerEmail.value, registerPassword.value);
    await handleLogin(registerUsername.value, registerPassword.value);
    showRegister.value = false;
    registerError.value = "";
  } catch (err) {
    console.error("Register error:", err.response?.data || err.message);
    if (err.response?.data) {
      // собираем сообщения от API и показываем
      registerError.value = Object.values(err.response.data)
        .flat()
        .join("\n");
    } else {
      registerError.value = "Registration failed";
    }
  }
};

const handleLogout = () => {
  logout();
  isLoggedIn.value = false;
  username.value = "";
  localStorage.removeItem("username");
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #455a64;
  color: white;
  padding: 10px 20px;
  border-radius: 0 0 10px 10px;
}
h3 {
    color:black;
}
.logo {
  font-size: 20px;
  font-weight: bold;
}

.auth-buttons button {
  margin-left: 10px;
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  background: #27c7b8;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.auth-buttons button:hover {
  background: #1fa699;
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal-content input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.actions {
  display: flex;
  justify-content: space-between;
}

.actions button {
  flex: 1;
  margin: 0 4px;
  padding: 8px;
  border-radius: 6px;
}

.actions button.secondary {
  background: #ccc;
  color: black;
}

.error {
  color: red;
  font-size: 13px;
  text-align: center;
}
</style>
