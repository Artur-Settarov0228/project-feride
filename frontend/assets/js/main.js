const API_BASE = `http://${window.location.hostname}:8000/api/v1`;

let currentUser = null;
let cartItems = [];
let allProducts = [];

document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    loadCategories();
    checkAuth();
    initEvents();
    initScrollAnimations();
    updateWishlistCount();
});

function initEvents() {
    // Auth
    const authBtn = document.getElementById('authBtn');
    if (authBtn) {
        authBtn.addEventListener('click', () => {
            if (currentUser) {
                if (confirm('Tizimdan chiqmoqchimisiz?')) {
                    localStorage.removeItem('token');
                    location.reload();
                }
            } else {
                showModal(document.getElementById('authModal'));
            }
        });
    }

    // Cart
    const cartBtn = document.getElementById('cartBtn');
    if (cartBtn) {
        cartBtn.addEventListener('click', () => {
            if (!currentUser) {
                showModal(document.getElementById('authModal'));
                return;
            }
            showModal(document.getElementById('cartModal'));
        });
    }

    // Close Modals
    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', hideAllModals);
    });

    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) hideAllModals();
    });

    // Auth Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            if (tab === 'login') {
                document.getElementById('loginForm').style.display = 'block';
                document.getElementById('registerForm').style.display = 'none';
            } else {
                document.getElementById('loginForm').style.display = 'none';
                document.getElementById('registerForm').style.display = 'block';
            }
        });
    });

    // Category Filtering (Redirect to separate page)
    document.querySelectorAll('.cat-link, .cat-circle-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const cat = item.dataset.category;
            window.location.href = `categories.html?category=${encodeURIComponent(cat)}`;
        });
    });

    // Shop Now Scroll
    const shopNowBtn = document.querySelector('.shop-now-btn');
    if (shopNowBtn) {
        shopNowBtn.addEventListener('click', () => {
            document.querySelector('.products-section').scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Login Form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const phone = document.getElementById('loginPhone').value;
            const password = document.getElementById('loginPassword').value;

            try {
                const res = await fetch(`${API_BASE}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phone, password })
                });

                if (!res.ok) throw new Error('Ma\'lumotlar noto\'g\'ri');
                
                const data = await res.json();
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('admin_token', data.access_token); // For admin dashboard compatibility
                
                // Fetch profile to check role
                const meRes = await fetch(`${API_BASE}/auth/me`, {
                    headers: { 'Authorization': `Bearer ${data.access_token}` }
                });
                const user = await meRes.json();
                
                if (user.is_admin) {
                    window.location.href = 'admin.html';
                } else {
                    location.reload();
                }
            } catch (err) {
                alert(err.message);
            }
        });
    }

    // Register Form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const full_name = document.getElementById('regName').value;
            const phone = document.getElementById('regPhone').value;
            const password = document.getElementById('regPassword').value;
            const role = document.getElementById('regRole') ? document.getElementById('regRole').value : 'user';

            try {
                const res = await fetch(`${API_BASE}/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ full_name, phone, password, is_seller: role === 'seller' })
                });

                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || 'Ro\'yxatdan o\'tishda xatolik');
                }
                
                alert('Muvaffaqiyatli ro\'yxatdan o\'tdingiz! Endi tizimga kiring.');
                document.querySelector('.tab-btn[data-tab="login"]').click();
            } catch (err) {
                alert(err.message);
            }
        });
    }

    // Add Product Form
    const addProductForm = document.getElementById('addProductForm');
    if (addProductForm) {
        addProductForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const productData = {
                name: document.getElementById('prodName').value,
                description: document.getElementById('prodDesc').value,
                price: parseFloat(document.getElementById('prodPrice').value),
                old_price: document.getElementById('prodOldPrice').value ? parseFloat(document.getElementById('prodOldPrice').value) : null,
                category: document.getElementById('prodCat').value,
                image_url: document.getElementById('prodImage').value,
                badge: document.getElementById('prodBadge').value || null,
                delivery_info: "Ertaga"
            };

            const token = localStorage.getItem('token') || localStorage.getItem('admin_token');
            try {
                const res = await fetch(`${API_BASE}/products/`, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(productData)
                });

                if (!res.ok) {
                    const errorText = await res.text();
                    throw new Error('Xatolik yuz berdi: ' + errorText);
                }
                
                alert('Mahsulot muvaffaqiyatli qo\'shildi!');
                window.location.href = 'index.html';
            } catch (err) {
                alert(err.message);
            }
        });
    }

    // Confirm Order
    const confirmOrderBtn = document.getElementById('confirmOrderBtn');
    if (confirmOrderBtn) {
        confirmOrderBtn.addEventListener('click', async () => {
            if (cartItems.length === 0) return;
            
            const name = document.getElementById('orderName').value;
            const phone = document.getElementById('orderPhone').value;
            const location = document.getElementById('orderLocation').value;

            if (!name || !phone || !location) {
                alert('Iltimos, barcha maydonlarni to\'ldiring!');
                return;
            }

            const token = localStorage.getItem('token');
            try {
                const res = await fetch(`${API_BASE}/cart/checkout`, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}` 
                    },
                    body: JSON.stringify({ name, phone, location })
                });

                if (!res.ok) throw new Error('Buyurtmani tasdiqlashda xatolik');
                
                const data = await res.json();
                alert('Buyurtmangiz qabul qilindi! Telegram botga yo\'naltirilmoqdasiz.');
                
                // Redirect to Telegram Bot
                window.open('https://t.me/YourBotName', '_blank');
                
                hideAllModals();
                loadCart();
            } catch (err) {
                alert(err.message);
            }
        });
    }

    // Qidiruv
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const filtered = allProducts.filter(p => 
                p.name.toLowerCase().includes(query) || 
                p.description.toLowerCase().includes(query)
            );
            renderProducts(filtered);
        });
    }
}

function showModal(modal) {
    if (!modal) return;
    modal.style.display = 'flex';
    setTimeout(() => modal.classList.add('show'), 10);
}

function hideAllModals() {
    document.querySelectorAll('.modal').forEach(m => {
        m.classList.remove('show');
        setTimeout(() => m.style.display = 'none', 400);
    });
}

async function loadProducts() {
    try {
        const res = await fetch(`${API_BASE}/products/`);
        allProducts = await res.json();
        renderProducts(allProducts);
    } catch (err) {
        console.error("Products load error", err);
    }
}

async function loadCategories() {
    try {
        const res = await fetch(`${API_BASE}/products/categories`);
        const categories = await res.json();
        renderCategories(categories);
    } catch (err) {
        console.error("Categories load error", err);
    }
}

function renderCategories(categories) {
    const nav = document.getElementById('categoriesNav');
    if (nav) {
        // Keep "Barchasi"
        nav.innerHTML = '<a href="#" class="cat-link active" data-category="Barchasi">Barchasi</a>' + 
            categories.map(cat => `<a href="#" class="cat-link" data-category="${cat.name}">${cat.name}</a>`).join('');
        
        // Re-attach listeners
        nav.querySelectorAll('.cat-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const cat = link.dataset.category;
                window.location.href = `categories.html?category=${encodeURIComponent(cat)}`;
            });
        });
    }

    const categoriesList = document.getElementById('categoriesList');
    if (categoriesList) {
        categoriesList.innerHTML = categories.map(cat => `
            <div class="category-card" onclick="window.location.href='categories.html?category=${encodeURIComponent(cat.name)}'">
                <img src="${cat.image_url || 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600&q=80'}" alt="">
                <div class="category-card-info">
                    <h3>${cat.name}</h3>
                    <span>Kolleksiyani ko'rish</span>
                </div>
            </div>
        `).join('');
    }

    const circleGrid = document.querySelector('.category-circles');
    if (circleGrid) {
        circleGrid.innerHTML = categories.map(cat => `
            <div class="cat-circle-item" data-category="${cat.name}">
                <div class="cat-circle-img"><img src="${cat.image_url || 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=300&q=80'}" alt=""></div>
                <span>${cat.name}</span>
            </div>
        `).join('');

        circleGrid.querySelectorAll('.cat-circle-item').forEach(item => {
            item.addEventListener('click', () => {
                const cat = item.dataset.category;
                window.location.href = `categories.html?category=${encodeURIComponent(cat)}`;
            });
        });
    }
}

function filterProducts(cat) {
    const titleEl = document.getElementById('currentCategoryTitle');
    if (titleEl) {
        titleEl.innerText = cat === 'Barchasi' ? 'Premium Mahsulotlar' : cat;
    }
    const filtered = cat === 'Barchasi' ? allProducts : allProducts.filter(p => p.category === cat);
    renderProducts(filtered);
    
    const section = document.querySelector('.products-section');
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function renderProducts(products) {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;
    
    if (products.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 100px; color: #888;">Bu turkumda mahsulotlar topilmadi.</div>';
        return;
    }

    grid.innerHTML = products.map((p, index) => {
        const isWishlisted = localStorage.getItem(`wishlist_${p.id}`) ? 'active' : '';
        return `
            <div class="product-card" style="transition-delay: ${index * 0.1}s">
                <div class="product-img-wrap">
                    ${p.badge ? `<div class="badge">${p.badge}</div>` : ''}
                    <button class="wishlist-btn ${isWishlisted}" data-id="${p.id}"><i class="far fa-heart"></i></button>
                    <img src="${p.image_url}" alt="${p.name}" onclick="goToDetails(${p.id})">
                    <div class="product-overlay">
                        <button class="quick-add" data-id="${p.id}">Savatga qo'shish</button>
                    </div>
                </div>
                <div class="product-info" onclick="goToDetails(${p.id})">
                    <div class="p-cat">${p.category}</div>
                    <div class="p-title">${p.name}</div>
                    <div class="p-price">
                        <span class="p-current">${p.price.toLocaleString()} so'm</span>
                        ${p.old_price ? `<span class="p-old">${p.old_price.toLocaleString()} so'm</span>` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');

    // Trigger animation
    setTimeout(() => {
        grid.querySelectorAll('.product-card').forEach(card => card.classList.add('visible'));
    }, 100);

    grid.querySelectorAll('.quick-add').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            addToCart(btn.dataset.id);
        });
    });

    grid.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleWishlist(btn.dataset.id, btn);
        });
    });
}

function goToDetails(id) {
    window.location.href = `product-details.html?id=${id}`;
}

function toggleWishlist(id, btn) {
    const key = `wishlist_${id}`;
    if (localStorage.getItem(key)) {
        localStorage.removeItem(key);
        btn.classList.remove('active');
    } else {
        localStorage.setItem(key, 'true');
        btn.classList.add('active');
    }
    updateWishlistCount();
}

function updateWishlistCount() {
    const wishlistCount = document.getElementById('wishlistCount');
    if (wishlistCount) {
        const count = Object.keys(localStorage).filter(k => k.startsWith('wishlist_')).length;
        wishlistCount.innerText = count;
    }
}

async function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
        const res = await fetch(`${API_BASE}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            currentUser = await res.json();
            const authText = document.getElementById('authText');
            if (authText) {
                authText.innerText = currentUser.full_name.split(' ')[0];
            }
            loadCart();
        } else {
            localStorage.removeItem('token');
        }
    } catch (err) {}
}

async function addToCart(id) {
    if (!currentUser) {
        showModal(document.getElementById('authModal'));
        return;
    }
    const token = localStorage.getItem('token');
    try {
        await fetch(`${API_BASE}/cart/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({ product_id: parseInt(id), quantity: 1 })
        });
        alert('Savatga qo\'shildi!');
        loadCart();
    } catch (err) {}
}

async function loadCart() {
    const token = localStorage.getItem('token');
    try {
        const res = await fetch(`${API_BASE}/cart/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        cartItems = await res.json();
        updateCartUI();
    } catch (err) {}
}

function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    if (cartCount) {
        cartCount.innerText = cartItems.reduce((a, b) => a + b.quantity, 0);
    }
    const list = document.getElementById('cartItemsList');
    if (!list) return;
    
    let total = 0;
    
    if (cartItems.length === 0) {
        list.innerHTML = '<div style="text-align: center; padding: 40px; color: #888;">Savatingiz bo\'sh.</div>';
        document.getElementById('cartTotalPrice').innerText = '0 so\'m';
        return;
    }

    list.innerHTML = cartItems.map(item => {
        total += item.product.price * item.quantity;
        return `
            <div class="cart-item">
                <img src="${item.product.image_url}" alt="">
                <div class="cart-item-info">
                    <h4>${item.product.name}</h4>
                    <p>${item.product.category}</p>
                    <div style="display: flex; align-items: center; gap: 15px; margin-top: 10px;">
                        <span style="font-weight: 700;">${item.product.price.toLocaleString()} so'm</span>
                        <div style="display: flex; align-items: center; gap: 10px; background: #f1f5f9; padding: 5px 12px; border-radius: 20px;">
                            <button onclick="decrementFromCart(${item.product.id})" style="border: none; background: none; cursor: pointer; color: #64748b;"><i class="fas fa-minus"></i></button>
                            <span style="font-weight: 700; color: #0f172a;">${item.quantity}</span>
                            <button onclick="addToCart(${item.product.id})" style="border: none; background: none; cursor: pointer; color: #0f172a;"><i class="fas fa-plus"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    document.getElementById('cartTotalPrice').innerText = total.toLocaleString() + " so'm";
}

async function decrementFromCart(id) {
    const token = localStorage.getItem('token');
    try {
        await fetch(`${API_BASE}/cart/decrement/${id}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        loadCart();
    } catch (err) {}
}

function initScrollAnimations() {
    const observerOptions = { threshold: 0.1 };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-slide-up').forEach(el => observer.observe(el));
}
