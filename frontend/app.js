const API_BASE = "http://localhost:8000";

let state = {
  user: null,
  token: localStorage.getItem("microshop_token") || "dev-mock-token",
  userId: parseInt(localStorage.getItem("microshop_user_id") || "1"),
  categories: [],
  products: [],
  cart: { items: [], total_price: 0 },
  activeCategory: null,
  searchQuery: "",
  isDebug: true
};

document.addEventListener("DOMContentLoaded", () => {
  initApp();
});

async function initApp() {
  await checkHealth();
  await loadCategories();
  await loadProducts();
  await loadCart();
  setupEventListeners();
}

async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    const data = await res.json();
    state.isDebug = data.debug_mode ?? true;

    const badge = document.getElementById("debug-badge");
    if (badge) {
      badge.textContent = state.isDebug ? "DEBUG: TRUE" : "PROD MODE";
      badge.style.background = state.isDebug ? "rgba(239, 68, 68, 0.2)" : "rgba(16, 185, 129, 0.2)";
      badge.style.color = state.isDebug ? "#fca5a5" : "#6ee7b7";
    }
  } catch (e) {
    console.warn("Gateway health check failed:", e);
  }
}

async function loadCategories() {
  try {
    const res = await fetch(`${API_BASE}/api/v1/categories`);
    if (res.ok) {
      state.categories = await res.json();
      renderCategories();
    }
  } catch (e) {
    console.error("Failed loading categories:", e);
  }
}

function renderCategories() {
  const container = document.getElementById("categories-container");
  if (!container) return;

  let html = `<button class="cat-pill ${state.activeCategory === null ? 'active' : ''}" onclick="selectCategory(null)">All Items</button>`;
  state.categories.forEach(cat => {
    html += `<button class="cat-pill ${state.activeCategory === cat.id ? 'active' : ''}" onclick="selectCategory(${cat.id})">${cat.name}</button>`;
  });
  container.innerHTML = html;
}

function selectCategory(catId) {
  state.activeCategory = catId;
  renderCategories();
  loadProducts();
}

async function loadProducts() {
  try {
    let url = `${API_BASE}/api/v1/products?`;
    if (state.activeCategory) url += `category_id=${state.activeCategory}&`;
    if (state.searchQuery) url += `search=${encodeURIComponent(state.searchQuery)}&`;

    const res = await fetch(url);
    if (res.ok) {
      state.products = await res.json();
      renderProducts();
    }
  } catch (e) {
    console.error("Failed loading products:", e);
  }
}

function renderProducts() {
  const grid = document.getElementById("products-grid");
  if (!grid) return;

  if (state.products.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">No products found.</div>`;
    return;
  }

  grid.innerHTML = state.products.map(prod => `
    <div class="product-card">
      <img class="product-img" src="${prod.image_url || 'https://via.placeholder.com/400x250'}" alt="${prod.title}">
      <div class="product-info">
        <h3 class="product-title">${prod.title}</h3>
        <p class="product-desc">${prod.description}</p>
        <div class="product-bottom">
          <span class="product-price">$${prod.price.toFixed(2)}</span>
          <button class="btn btn-primary" onclick="addToCart(${prod.id})">
            + Add to Cart
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

async function loadCart() {
  try {
    const res = await fetch(`${API_BASE}/api/v1/cart/${state.userId}`);
    if (res.ok) {
      state.cart = await res.json();
      updateCartBadge();
    }
  } catch (e) {
    console.error("Failed loading cart:", e);
  }
}

function updateCartBadge() {
  const countEl = document.getElementById("cart-count");
  if (countEl) {
    const totalItems = state.cart.items ? state.cart.items.reduce((sum, i) => sum + i.quantity, 0) : 0;
    countEl.textContent = totalItems;
  }
}

async function addToCart(productId) {
  try {
    const res = await fetch(`${API_BASE}/api/v1/cart/${state.userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product_id: productId, quantity: 1 })
    });
    if (res.ok) {
      state.cart = await res.json();
      updateCartBadge();
      alert("Product added to cart!");
    } else {
      const err = await res.json();
      alert(err.detail || "Failed to add to cart");
    }
  } catch (e) {
    console.error("Add to cart failed:", e);
  }
}

function openCartModal() {
  renderCartModal();
  document.getElementById("cart-modal").classList.add("open");
}

function closeCartModal() {
  document.getElementById("cart-modal").classList.remove("open");
}

function renderCartModal() {
  const container = document.getElementById("cart-modal-body");
  if (!container) return;

  if (!state.cart.items || state.cart.items.length === 0) {
    container.innerHTML = `<p style="text-align: center; color: var(--text-muted); padding: 2rem;">Your cart is currently empty.</p>`;
    return;
  }

  let html = state.cart.items.map(item => `
    <div class="cart-item">
      <div>
        <strong>${item.title}</strong>
        <div style="font-size: 0.85rem; color: var(--text-muted);">$${item.price.toFixed(2)} x ${item.quantity}</div>
      </div>
      <div>
        <button class="btn btn-secondary" style="padding: 0.2rem 0.5rem;" onclick="removeFromCart(${item.product_id})">✕</button>
      </div>
    </div>
  `).join('');

  html += `
    <div class="cart-total">
      <span>Total:</span>
      <span style="color: var(--accent);">$${state.cart.total_price.toFixed(2)}</span>
    </div>
    <button class="btn btn-primary" style="width: 100%;" onclick="checkout()">Checkout Order</button>
  `;

  container.innerHTML = html;
}

async function removeFromCart(productId) {
  try {
    const res = await fetch(`${API_BASE}/api/v1/cart/${state.userId}/items/${productId}`, {
      method: "DELETE"
    });
    if (res.ok) {
      state.cart = await res.json();
      updateCartBadge();
      renderCartModal();
    }
  } catch (e) {
    console.error(e);
  }
}

async function checkout() {
  try {
    const headers = { "Content-Type": "application/json" };
    if (state.token) {
      headers["Authorization"] = `Bearer ${state.token}`;
    }

    const res = await fetch(`${API_BASE}/api/v1/orders`, {
      method: "POST",
      headers: headers
    });

    if (res.ok) {
      const order = await res.json();
      alert(`Order #${order.id} placed successfully! Total: $${order.total_price}`);
      await loadCart();
      closeCartModal();
    } else {
      const err = await res.json();
      alert(err.detail || "Checkout failed.");
    }
  } catch (e) {
    console.error("Checkout error:", e);
  }
}

function setupEventListeners() {
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    let debounce;
    searchInput.addEventListener("input", (e) => {
      clearTimeout(debounce);
      debounce = setTimeout(() => {
        state.searchQuery = e.target.value;
        loadProducts();
      }, 300);
    });
  }
}
