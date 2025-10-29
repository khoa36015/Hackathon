export const API_BASE = 'http://localhost:3000/api';

export async function register(username, password) {
  const res = await fetch(`${API_BASE}/register`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return await res.json();
}

export async function login(username, password) {
  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return await res.json();
}

export async function checkSession() {
  const res = await fetch(`${API_BASE}/check-session`, {
    method: 'GET',
    credentials: 'include'
  });
  return await res.json();
}

export async function logout() {
  const res = await fetch(`${API_BASE}/logout`, {
    method: 'POST',
    credentials: 'include'
  });
  return await res.json();
}