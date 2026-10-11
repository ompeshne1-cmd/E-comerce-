/**
 * HEDLUM CRAFT BEVERAGE SHOP JAVASCRIPT
 * Handles 3D can physics, cart drawers, flavor switching, and checkout AJAX
 */

document.addEventListener('DOMContentLoaded', () => {
    // State
    let currentPack = '12-Pack Case';
    let currentPrice = 14.99;
    let currentProductId = document.getElementById('heroAddToCartBtn')?.dataset.productId;

    // Elements
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const can3DWrapper = document.getElementById('can3DWrapper');
    const heroCanImg = document.getElementById('heroCanImg');
    const heroHeadline = document.getElementById('heroHeadline');
    const displayedPrice = document.getElementById('displayedPrice');
    const heroAddToCartBtn = document.getElementById('heroAddToCartBtn');
    const packPills = document.querySelectorAll('.pack-pill');
    const swatchBtns = document.querySelectorAll('.swatch-btn');
    
    // Drawers & Modals
    const cartBtn = document.getElementById('cartBtn');
    const cartDrawer = document.getElementById('cartDrawer');
    const closeCartBtn = document.getElementById('closeCartBtn');
    const cartBackdrop = document.getElementById('cartBackdrop');

    const shopNowBtn = document.getElementById('shopNowBtn');
    const catalogDrawer = document.getElementById('catalogDrawer');
    const closeCatalogBtn = document.getElementById('closeCatalogBtn');
    const catalogBackdrop = document.getElementById('catalogBackdrop');

    const accountBtn = document.getElementById('accountBtn');
    const accountModal = document.getElementById('accountModal');
    const closeAccountBtn = document.getElementById('closeAccountBtn');

    const checkoutModal = document.getElementById('checkoutModal');
    const closeCheckoutBtn = document.getElementById('closeCheckoutBtn');
    const proceedCheckoutBtn = document.getElementById('proceedCheckoutBtn');
    const checkoutForm = document.getElementById('checkoutForm');

    const orderSuccessModal = document.getElementById('orderSuccessModal');
    const keepShoppingBtn = document.getElementById('keepShoppingBtn');
    const toastPopup = document.getElementById('toastPopup');

    // -------------------------------------------------------------
    // 1. 3D Can Interactive Mouse Movement Physics
    // -------------------------------------------------------------
    if (can3DWrapper && heroCanImg) {
        can3DWrapper.addEventListener('mousemove', (e) => {
            const rect = can3DWrapper.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateY = ((x - centerX) / centerX) * 16;
            const rotateX = -((y - centerY) / centerY) * 14;

            heroCanImg.style.transform = `rotate(14deg) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
        });

        can3DWrapper.addEventListener('mouseleave', () => {
            heroCanImg.style.transform = `rotate(14deg) translateY(-8px)`;
        });
    }

    // -------------------------------------------------------------
    // 2. Pack Size Selector
    // -------------------------------------------------------------
    packPills.forEach(pill => {
        pill.addEventListener('click', () => {
            packPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            currentPack = pill.dataset.pack;
            currentPrice = parseFloat(pill.dataset.price);
            if (displayedPrice) {
                displayedPrice.textContent = `$${currentPrice.toFixed(2)}`;
            }
        });
    });

    // -------------------------------------------------------------
    // 3. Flavor Swatches Switcher
    // -------------------------------------------------------------
    swatchBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            swatchBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const newId = btn.dataset.id;
            const newImg = btn.dataset.img;
            const newHeadline = btn.dataset.headline;
            const newPrice = parseFloat(btn.dataset.price);

            currentProductId = newId;
            heroAddToCartBtn.dataset.productId = newId;

            // Smooth image swap with tilt transition
            heroCanImg.style.opacity = '0.3';
            heroCanImg.style.transform = 'rotate(0deg) scale(0.9)';
            
            setTimeout(() => {
                heroCanImg.src = newImg;
                heroCanImg.style.opacity = '1';
                heroCanImg.style.transform = 'rotate(14deg) translateY(-8px)';
            }, 180);

            if (heroHeadline) {
                heroHeadline.textContent = newHeadline;
            }

            // Reset pack to 12-pack price
            packPills.forEach(p => {
                if (p.dataset.pack === '12-Pack Case') {
                    p.classList.add('active');
                    currentPack = '12-Pack Case';
                    currentPrice = newPrice;
                    p.dataset.price = newPrice;
                } else if (p.dataset.pack === '4-Pack') {
                    p.classList.remove('active');
                    p.dataset.price = (newPrice * 0.45).toFixed(2);
                } else {
                    p.classList.remove('active');
                    p.dataset.price = (newPrice * 1.85).toFixed(2);
                }
            });

            if (displayedPrice) {
                displayedPrice.textContent = `$${newPrice.toFixed(2)}`;
            }
        });
    });

    // -------------------------------------------------------------
    // 4. Toast Notification Helper
    // -------------------------------------------------------------
    function showToast(msg) {
        if (!toastPopup) return;
        toastPopup.textContent = msg;
        toastPopup.classList.add('show');
        setTimeout(() => {
            toastPopup.classList.remove('show');
        }, 2600);
    }

    // -------------------------------------------------------------
    // 5. Drawer Controls
    // -------------------------------------------------------------
    function openCart() {
        cartDrawer?.classList.add('active');
        fetchCartData();
    }
    function closeCart() {
        cartDrawer?.classList.remove('active');
    }
    function openCatalog() {
        catalogDrawer?.classList.add('active');
    }
    function closeCatalog() {
        catalogDrawer?.classList.remove('active');
    }

    cartBtn?.addEventListener('click', openCart);
    closeCartBtn?.addEventListener('click', closeCart);
    cartBackdrop?.addEventListener('click', closeCart);

    shopNowBtn?.addEventListener('click', openCatalog);
    closeCatalogBtn?.addEventListener('click', closeCatalog);
    catalogBackdrop?.addEventListener('click', closeCatalog);

    window.openCatalog = openCatalog;

    // Account modal
    accountBtn?.addEventListener('click', () => accountModal?.classList.add('active'));
    closeAccountBtn?.addEventListener('click', () => accountModal?.classList.remove('active'));
    window.closeAccountModal = () => accountModal?.classList.remove('active');

    // -------------------------------------------------------------
    // 6. Cart AJAX Functions
    // -------------------------------------------------------------
    async function addToCart(productId, packSize, quantity = 1) {
        try {
            const resp = await fetch('/api/cart/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    product_id: productId,
                    pack_size: packSize,
                    quantity: quantity
                })
            });

            const data = await resp.json();
            if (data.success) {
                showToast(data.message);
                updateCartUI(data);
                openCart();
            } else {
                alert(data.error || 'Failed to add item to cart');
            }
        } catch (err) {
            console.error('Add to cart error:', err);
        }
    }

    // Quick add from Hero
    heroAddToCartBtn?.addEventListener('click', () => {
        addToCart(currentProductId, currentPack, 1);
    });

    // Add direct from Catalog drawer
    window.addToCartDirect = function(productId, packSize, price) {
        addToCart(productId, packSize, 1);
    };

    // Update Cart Item (Quantity / Remove)
    window.updateItemQty = async function(itemId, action) {
        try {
            const resp = await fetch('/api/cart/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    item_id: itemId,
                    action: action
                })
            });
            const data = await resp.json();
            if (data.success) {
                updateCartUI(data);
            }
        } catch (err) {
            console.error('Update item error:', err);
        }
    };

    async function fetchCartData() {
        try {
            const resp = await fetch('/api/cart/');
            const data = await resp.json();
            updateCartUI(data);
        } catch (err) {
            console.error('Fetch cart error:', err);
        }
    }

    function updateCartUI(data) {
        // Update header badges
        const cartCountEl = document.getElementById('cartItemCount');
        const drawerCountEl = document.getElementById('cartDrawerCount');
        if (cartCountEl) cartCountEl.textContent = data.total_items;
        if (drawerCountEl) drawerCountEl.textContent = `(${data.total_items} items)`;

        // Update Shipping Tracker
        const shippingMsg = document.getElementById('shippingMsg');
        const progressFill = document.getElementById('shippingProgressFill');
        if (shippingMsg && progressFill) {
            if (data.subtotal >= 35.0) {
                shippingMsg.innerHTML = '🎉 You unlocked <strong>FREE Shipping!</strong>';
                progressFill.style.width = '100%';
            } else {
                shippingMsg.innerHTML = `Add <strong>$${data.needed_for_free_ship.toFixed(2)}</strong> more for <strong>FREE SHIPPING!</strong>`;
                progressFill.style.width = `${data.progress_pct}%`;
            }
        }

        // Update Totals
        const subtotalEl = document.getElementById('cartSubtotalVal');
        const shippingEl = document.getElementById('cartShippingVal');
        const totalEl = document.getElementById('cartTotalVal');
        const checkoutBtnTotal = document.getElementById('checkoutTotalBtn');

        if (subtotalEl) subtotalEl.textContent = `$${data.subtotal.toFixed(2)}`;
        if (shippingEl) shippingEl.textContent = data.shipping === 0 ? 'FREE' : `$${data.shipping.toFixed(2)}`;
        if (totalEl) totalEl.textContent = `$${data.total.toFixed(2)}`;
        if (checkoutBtnTotal) checkoutBtnTotal.textContent = `$${data.total.toFixed(2)}`;

        // Render Cart Items List
        const itemsListContainer = document.getElementById('cartItemsList');
        if (!itemsListContainer) return;

        if (data.items.length === 0) {
            itemsListContainer.innerHTML = `
                <div class="empty-cart-state" id="emptyCartState">
                    <div class="empty-icon">🥤</div>
                    <h4>Your cooler is empty!</h4>
                    <p>Stock up on ice-cold Hedlum craft brew sodas.</p>
                    <button class="empty-shop-btn" onclick="openCatalog()">SHOP FLAVORS NOW</button>
                </div>
            `;
        } else {
            let html = '';
            data.items.forEach(item => {
                html += `
                    <div class="cart-item-row" data-item-id="${item.id}">
                        <div class="item-thumb" style="background: ${item.primary_color}22;">
                            <img src="${item.image_url}" alt="${item.name}">
                        </div>
                        <div class="item-details">
                            <h5 class="item-title">${item.name}</h5>
                            <span class="item-pack">${item.pack_size}</span>
                            <span class="item-unit-price">$${item.unit_price.toFixed(2)}</span>
                        </div>
                        <div class="item-qty-actions">
                            <div class="qty-stepper">
                                <button type="button" class="qty-btn" onclick="updateItemQty('${item.id}', 'decrease')">−</button>
                                <span class="qty-val">${item.quantity}</span>
                                <button type="button" class="qty-btn" onclick="updateItemQty('${item.id}', 'increase')">+</button>
                            </div>
                            <span class="item-subtotal">$${item.subtotal.toFixed(2)}</span>
                            <button class="item-remove-btn" onclick="updateItemQty('${item.id}', 'remove')" title="Remove">✕</button>
                        </div>
                    </div>
                `;
            });
            itemsListContainer.innerHTML = html;
        }
    }

    // -------------------------------------------------------------
    // 7. Checkout Flow
    // -------------------------------------------------------------
    proceedCheckoutBtn?.addEventListener('click', () => {
        closeCart();
        checkoutModal?.classList.add('active');
    });

    closeCheckoutBtn?.addEventListener('click', () => {
        checkoutModal?.classList.remove('active');
    });

    checkoutForm?.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('custName')?.value;
        const email = document.getElementById('custEmail')?.value;
        const address = document.getElementById('custAddress')?.value;
        const city = document.getElementById('custCity')?.value;
        const postal_code = document.getElementById('custZip')?.value;

        try {
            const resp = await fetch('/api/checkout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    name, email, address, city, postal_code
                })
            });

            const result = await resp.json();
            if (result.success) {
                checkoutModal?.classList.remove('active');
                
                // Show order success modal
                const successOrderNum = document.getElementById('successOrderNum');
                if (successOrderNum) {
                    successOrderNum.textContent = `ORDER #${result.order_number}`;
                }
                orderSuccessModal?.classList.add('active');
                
                // Reset cart UI
                fetchCartData();
            } else {
                alert(result.error || 'Checkout failed. Please try again.');
            }
        } catch (err) {
            console.error('Checkout error:', err);
        }
    });

    keepShoppingBtn?.addEventListener('click', () => {
        orderSuccessModal?.classList.remove('active');
    });
});
