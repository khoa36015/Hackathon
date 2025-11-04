export const API_AUTH = 'http://localhost:3000/api';
export const API_PROVINCE = 'http://localhost:1311/api';

export async function register(username, password) {
  const res = await fetch(`${API_AUTH}/register`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return await res.json();
}

export async function login(username, password) {
  const res = await fetch(`${API_AUTH}/login`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return await res.json();
}

export async function checkSession() {
  const res = await fetch(`${API_AUTH}/check-session`, {
    method: 'GET',
    credentials: 'include'
  });
  return await res.json();
}

export async function logout() {
  const res = await fetch(`${API_AUTH}/logout`, {
    method: 'POST',
    credentials: 'include'
  });
  return await res.json();
}

export async function getProvinces() {
  const res = await fetch(`${API_PROVINCE}/provinces`, {
    method: 'GET',
    credentials: 'include'
  });
  return await res.json();
}

export async function getDetailProvice() {
  const res = await fetch(`${API_PROVINCE}/province/<province_id>`, {
    method: 'GET',
    credentials: 'include'
  });
  return await res.json();
}

export async function sendAgentMessage(message) {
  const res = await fetch('http://127.0.0.1:8000/api/ai/agent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  return await res.json();
}
