# 🍽️ Koya Restaurant Backend

A RESTful backend API built with Django and Django REST Framework to power the Koya Restaurant web application. It provides authentication, menu management, food ordering, reservations, shopping cart functionality, wishlist management, and other core restaurant services.

## 🚀 Features

- User registration and authentication
- JWT authentication
- Menu and category management
- Shopping cart
- Wishlist
- Food ordering
- Reservation system
- RESTful APIs
- File uploads
- Admin management

## 🛠️ Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL (Production)
- SQLite (Development)
- Gunicorn
- PythonAnywhere
- JWT Authentication

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/menu/` | Retrieve restaurant menu |
| `/api/orders/` | Place and manage orders |
| `/api/cart/` | Shopping cart |
| `/api/accounts/register/` | Register a new user |
| `/api/accounts/login/` | User login |
| `/api/reservation/` | Create and manage reservations |
| `/api/wishlist/` | Wishlist management |

## ⚙️ Installation

```bash
git clone https://github.com/Olukoyataiwohammed/koya-restaurant-backend.git

cd koya-restaurant-backend

python -m venv venv

# Windows
venv\Scripts\activate



pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

## 🌐 Live Application

**Frontend**

https://koya-restaurant.vercel.app/



## 👨‍💻 Author
- **Taiwo Olukoya**

**Taiwo Olukoya**

GitHub: https://github.com/Olukoyataiwohammed
