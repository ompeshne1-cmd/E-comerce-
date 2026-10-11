# HEDLUM — Craft Soft Drink E-Commerce Website

A production-ready, full-stack e-commerce application built strictly to replicate the exact design from your screenshot.

---

## 🌟 Key Features

1. **Exact Screenshot Design Replication:**
   - **Signature Yellow Background:** Golden mustard background (`#DBAE00` / `#EECB3A`) with sleek black tablet showcase border.
   - **Organic Dripping Wave Transition:** Beautiful fluid SVG drip transition blending into a misty rocky waterfall scene.
   - **Giant Typography:** Bold, condensed uppercase **"HEDLUM"** brand title.
   - **Authentic Hero Elements:**
     - Standing cartoon hand mascot giving the rock-on horn sign 🤘
     - Exact uppercase bold text: `LOREM IPSUM CONSECTETUR DOLOR SIT CONSECT.`
     - Pure white 4-point sparkle star ✨
     - Announcement bar: `"Free shipping on all orders over $35"`
     - Sleek navigation with `≈ SHOP NOW`, `☺ account`, and `🛒 cart` pill badge.
2. **Interactive 3D Can Experience:**
   - 3D angled golden craft beverage can (*"BREWED TO BE WILD • NON-ALCOHOLIC BREW"*).
   - Mouse-movement 3D parallax tilt physics!
   - Real-time **Flavor Switcher** (Original Golden Malt, Ruby Berry Crush, Emerald Citrus Lime, Blue Glacier Razz).
   - Pack size selector (4-Pack, 12-Pack Case, 24-Pack Party Pack) with dynamic price calculation.
3. **Full-Featured E-Commerce Mechanics:**
   - **Slide-out Cart Drawer:** Real-time quantity controls (`+` / `−` / remove) with animated item thumbnails.
   - **Dynamic Free Shipping Progress Bar:** Shows progress toward the $35 threshold.
   - **Slide-out Shop Catalog Drawer:** Triggered by `≈ SHOP NOW` to browse all soda flavors.
   - **Simulated Checkout Modal:** Collects customer details and shipping address.
   - **Order Confirmation:** Issues unique order numbers (`#HD-XXXXXX`) and saves them in the database.
   - **Django Admin Interface:** Full administration dashboard at `/admin/`.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12, Django 6.1
- **Database:** MySQL 8.0 (configured with `PyMySQL`), with automatic SQLite fallback
- **Frontend:** Semantic HTML5, Custom Responsive CSS3, Vanilla JavaScript (ES6+)
- **Version Control:** Git initialized with initial commits

---

## 🚀 Quick Start Guide

### 1. Run the Development Server
The server is already running on:
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

To start it manually at any time:
```powershell
cd "C:\Users\ASUS\.gemini\antigravity\scratch\hedlum_ecommerce"
python manage.py runserver 127.0.0.1:8000
```

### 2. Django Admin Access
Manage products, categories, orders, and cart items at:
- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username:** `admin`
- **Password:** `admin123`

---

## 🗄️ Connecting to MySQL

Your Windows MySQL service (`MySQL80`) is already running. To connect the website to your local MySQL database:

1. Run the interactive setup script:
   ```powershell
   python setup_mysql.py
   ```
2. Enter your MySQL password when prompted. The script will automatically:
   - Create the `hedlum_db` database
   - Save credentials to `.env`
   - Run Django migrations to MySQL

Alternatively, create a `.env` file in the project root:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=hedlum_db
```
When MySQL credentials are configured, Django connects to MySQL automatically. If no password is provided, it runs on SQLite so you can develop immediately without setup blocks.

---

## 📁 Project Structure

```
hedlum_ecommerce/
├── hedlum_project/          # Django Project Configuration
│   ├── settings.py         # Configured with MySQL & PyMySQL
│   ├── urls.py             # Root URL routing
│   └── wsgi.py
├── shop/                   # Main Shop Application
│   ├── models.py           # Product, Category, Cart, CartItem, Order, OrderItem
│   ├── views.py            # Cart, checkout, and home views
│   ├── urls.py             # Application URLs
│   ├── admin.py            # Django Admin configuration
│   ├── management/         # Data seed commands (seed_products.py)
│   ├── static/shop/
│   │   ├── css/style.css   # Pixel-accurate layout & styling
│   │   ├── js/app.js       # 3D can physics, AJAX cart, checkout
│   │   └── images/         # Hedlum cans, mascot, and waterfall background
│   └── templates/shop/
│       └── index.html      # Responsive hero showcase matching screenshot
├── setup_mysql.py          # Interactive MySQL connection wizard
├── manage.py
└── README.md
```
