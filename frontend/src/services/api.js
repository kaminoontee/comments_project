import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

// сохранить токен
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem("token", token);
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
  }
};

// получить токен
export const getAuthToken = () => {
  return localStorage.getItem("token");
};

// проверка авторизации
export const isAuthenticated = () => {
  return !!localStorage.getItem("token");
};

// логин
export const login = async (username, password) => {
  const response = await api.post("token/", { username, password });
  const token = response.data.access;
  setAuthToken(token);
  return response.data;
};

// регистрация
export const register = async (username, email, password) => {
  return await api.post("register/", { username, email, password });
};

// логаут
export const logout = () => {
  setAuthToken(null);
};
