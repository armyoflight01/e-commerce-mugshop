# KILN & CO. — Artisanal Mug E-Commerce System

A full-stack, responsive e-commerce web application built with **Python 3.15**, **Django 6.1**, and **Tailwind CSS**, designed specifically for artisanal ceramic coffee mugs, insulated travel tumblers, and vintage enamel drinkware.

---

## ☕ Key Features

1. **Storefront & Catalog**
   - **Hero Showcase:** Highlighting kiln drops, small-batch releases, and craftsmanship trust badges.
   - **Category Filtering:** Artisanal Ceramic, Insulated Travel Tumblers, Vintage Enamel Campfire, and Minimalist & Espresso cups.
   - **Sorting & Search:** Filter by keyword, price range, rating, newest arrivals, and bestsellers.

2. **Product Detail Page**
   - High-resolution gallery and thumbnail switcher.
   - Technical specifications (capacity in ml/oz, dimensions, dishwasher/microwave safety, materials).
   - **Personalized Custom Laser Engraving:** Customers can enter custom names, dates, or quotes on mugs.
   - Verified customer review listing and instant submission form with 1–5 star ratings.

3. **Shopping Cart & Checkout**
   - **Live Cart Badge:** Real-time counter across all pages.
   - **Free Shipping Progress Meter:** Dynamic goal-tracker for free shipping ($50 threshold).
   - **Discount Coupons:** Built-in discount system (`MUG10` for 10% off, `CERAMIC20` for 20% off).
   - **Full Checkout Flow:** Collects shipping details, order notes, and payment preference (Cash on Delivery, Mock Card, Bank Transfer).
   - **Order Confirmation & Invoicing:** Printable receipt with a unique order tracking code (e.g. `MUG-XXXXXXXX`).

4. **Order Tracking**
   - Dedicated tracking page (`/track/`) with a 4-step delivery pipeline (Confirmed → Packing → In Transit → Delivered).

5. **Backoffice / Admin Panel**
   - Django Admin integration at `/admin/` for managing products, categories, stock levels, orders, and customer reviews.

---

## 🚀 How to Run the Website

```powershell
cd "c:\xampp\htdocs\FULL-STACK WEB PYTHON\newproject"
python manage.py runserver
```

Open your browser to:
- **Storefront:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Shop Catalog:** [http://127.0.0.1:8000/shop/](http://127.0.0.1:8000/shop/)
- **Shopping Cart:** [http://127.0.0.1:8000/cart/](http://127.0.0.1:8000/cart/)
- **Order Tracking:** [http://127.0.0.1:8000/track/](http://127.0.0.1:8000/track/)
- **Admin Portal:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📦 Database Management & Seeding

To re-seed sample products, categories, and customer reviews at any time:
```powershell
python manage.py seed_store
```

To create a new administrator account:
```powershell
python manage.py createsuperuser
```
Or to update the password for the existing user `russellevan`:
```powershell
python manage.py changepassword russellevan
```
