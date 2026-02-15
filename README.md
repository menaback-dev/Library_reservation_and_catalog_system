# Community Library Catalog & Reservation System

![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-9.0-red)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-cyan)

A **RESTful API** built with Django and Django REST Framework for managing a community library reservation and catalog. Users can browse and search the book catalog, while authenticated users can reserve books. If a book is unavailable, users are added to a queue and automatically promoted when copies become available.

This is my **ALX Back-End development Capstone Project**.

## Features

- **User Authentication**: JWT-based login (using `djangorestframework-simplejwt`)
- **Book Catalog**:
  - Search books by title, author, or ISBN
  - Filter by category
  - Admin CRUD for books and categories
- **Reservation System**:
  - Reserve an available book (decrements available copies)
  - Automatic queuing when no copies are available
  - Queue position tracking
  - Cancel reservation → promotes next user in queue if applicable
- **Interactive API Documentation**: Swagger UI powered by `drf-spectacular`
- **Admin Panel**: Full Django admin interface for managing data

## Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Authentication**: SimpleJWT
- **API Documentation**: drf-spectacular
- **Database**: SQLite (development), easily switchable to PostgreSQL/MySQL
- **Filtering & Search**: Django Filter, SearchFilter, OrderingFilter

## Project Structure
  - library_reservation_and_catalog_system/
  - ├── books/                  # Book and Category models, serializers, views
  - ├── reservations/           # Reservation model with queue logic
  - ├── users/                  # (Placeholder for future custom user)
  - ├── library_reservation_and_catalog_system/
  - │   ├── settings.py
  - │   ├── urls.py             # Main router and JWT endpoints
  - │   └── ...
  - ├── manage.py
  - └── db.sqlite3              # Development database

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/library-reservation-and-catalog-system.git
   cd library-reservation-and-catalog-system

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac # or
   venv\Scripts\activate       # Windows

3. **Install dependencies**
   ```bash
    pip install -r requirements.txt
(If no requirements.txt yet, install manually:)

    pip install django djangorestframework djangorestframework-simplejwt drf-spectacular django-filter
4. **Run migrations**
   ```bash
    python manage.py makemigrations
    python manage.py migrate
5. **Create a superuser (for admin access)**
   ```bash
    python manage.py createsuperuser
6. **Run the development server**
   ```bash
    python manage.py runserver

## Usage

- Admin Panel: http://127.0.0.1:8000/admin/ → Add categories, books, and view reservations
- API Documentation (Swagger UI): http://127.0.0.1:8000/api/docs/
- Key Endpoints:
    - POST /api/token/ → Get JWT token
    - GET /api/books/ → List and search books
    - GET /api/categories/ → List categories (admin only for CRUD)
    - POST /api/reservations/ → Create reservation (handles reserve/queue)
    - POST /api/reservations/{id}/cancel/ → Cancel reservation

## Sample Data
The admin panel is pre-seeded with real books (e.g., Things Fall Apart, Beneath the Lion's Gaze, Sapiens) across categories like Fiction, African Literature, and Non-Fiction for easy testing.

## License
This project is open-source under the MIT License. Feel free to fork and use it!

## Author
Abdulmenan Amin
ALX Africa Back-End Development Student
