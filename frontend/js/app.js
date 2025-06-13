const API_BASE = 'http://localhost:8000';

function login() {
  // Redirect to Discord OAuth2 URL
  window.location.href = '/api/login';
}

async function fetchProfile(id) {
  const res = await fetch(`${API_BASE}/profile/${id}`);
  return res.json();
}

let cart = [];

function renderCart() {
  const container = document.getElementById('cart');
  if (!container) return;
  container.innerHTML = '';
  cart.forEach(item => {
    const li = document.createElement('li');
    li.className = 'cart-item';
    li.textContent = `${item.name} x${item.qty}`;
    container.appendChild(li);
  });
}

function addToCart(product, qtyInput) {
  const qty = parseInt(qtyInput.value);
  if (!qty) return;
  const existing = cart.find(c => c.id === product.id);
  if (existing) {
    existing.qty += qty;
  } else {
    cart.push({ id: product.id, name: product.name, qty });
  }
  renderCart();
  qtyInput.value = 1;
}

async function loadShop() {
  const list = document.getElementById('shop');
  if (!list) return;
  const res = await fetch(`${API_BASE}/shop`);
  const items = await res.json();
  items.forEach(item => {
    const li = document.createElement('li');
    li.className = 'product';
    li.innerHTML = `
      <img src="${item.logo}" alt="${item.name}" class="logo">
      <div class="info">
        <h3>${item.name}</h3>
        <p class="price">${item.price} BC</p>
        <input type="number" min="1" value="1" class="qty">
        <button class="add">Dodaj</button>
      </div>
    `;
    list.appendChild(li);
    const qtyInput = li.querySelector('.qty');
    li.querySelector('.add').addEventListener('click', () => addToCart(item, qtyInput));
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('login');
  if (loginBtn) loginBtn.addEventListener('click', login);
  loadShop();
});
