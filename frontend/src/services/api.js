import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// ✅ автоматически вставляем токен из localStorage в каждый запрос
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// сохранить токены
export const setTokens = (access, refresh) => {
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
};

// получить access токен
export const getAuthToken = () => {
  return localStorage.getItem("access");
};

// проверка авторизации
export const isAuthenticated = () => {
  return !!localStorage.getItem("access");
};

// логин
export const login = async (username, password) => {
  const response = await api.post("token/", { username, password });
  const { access, refresh } = response.data;
  setTokens(access, refresh);
  return response.data;
};

// регистрация
export const register = async (username, email, password) => {
  return await api.post("register/", { username, email, password });
};

// логаут
export const logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};
