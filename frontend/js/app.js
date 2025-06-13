const API_BASE = 'http://localhost:8000';

function login() {
  // Redirect to Discord OAuth2 URL
  window.location.href = '/api/login';
}

async function fetchProfile(id) {
  const res = await fetch(`${API_BASE}/profile/${id}`);
  return res.json();
}

document.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('login');
  if (loginBtn) loginBtn.addEventListener('click', login);
});
