# Community Library Catalog & Reservation System

![Django](https://img.shields.io/badge/Django-6.0.1-green?logo=django)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.16.1-red)
![Python](https://img.shields.io/badge/Python-3.13.7-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-cyan)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![PythonAnywhere](https://img.shields.io/badge/Deployed%20On-PythonAnywhere-blue)

**Live API Documentation (Swagger UI):**  
https://libraryreservation.pythonanywhere.com/api/docs/

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
- **Testing**: Basic unit tests for reservation logic (creation, queuing, cancelling with promotion).
- **Admin Panel**: Full Django admin interface for managing data

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: SimpleJWT
- **API Documentation**: drf-spectacular
- **Database**: SQLite
- **Filtering & Search**: Django Filter, SearchFilter, OrderingFilter

## Live Demo

- **Swagger UI:**  
  https://libraryreservation.pythonanywhere.com/api/docs/

- **Django Admin Panel** (login required):  
  https://libraryreservation.pythonanywhere.com/admin/

- **Browsable API examples**:
  - Books list: https://libraryreservation.pythonanywhere.com/api/books/
  - Categories: https://libraryreservation.pythonanywhere.com/api/categories/

## Core Entities

- **Category**: Simple model for book genres (e.g., Fiction, African Literature).
- **Book**: Includes title, author, ISBN, category, total_copies, available_copies, cover_image_url.
- **Reservation**: Links user and book, with status (reserved, queued, cancelled, returned), queue_position (for queued only), reserved_at timestamp.

## Key Business Rules

- **Reservation Creation**:
- If available_copies > 0 → status = 'reserved', decrement copies
- If available_copies = 0 → status = 'queued', assign next position (1, 2, 3...)
- One active reservation per user per book (partial unique constraint)

- **Cancellation**:
- Reserved → return copy (+1 available), promote first queued user to reserved
- Queued → shift remaining queue positions down
- Renumber queue after every change (safe & predictable)

- **Permissions**:
- Books & categories → read-only for everyone, CRUD for admins only
- Reservations → authenticated users only, own reservations only
- Cancel action → restricted to reservation owner

## How to Test the API Using Swagger UI

Live Swagger URL:
https://libraryreservation.pythonanywhere.com/api/docs/

# Step-by-Step Guide

- Open the Swagger UI
Visit: https://libraryreservation.pythonanywhere.com/api/docs/
1. Authorize (Login)
Click the green Authorize button (top-right corner).
In the popup, select JWT Bearer (http, bearer).
First, create a test user if needed:
- Expand POST /api/register/ → Try it out → Enter:JSON{
  "username": "mentor_test",
  "email": "mentor@example.com",
  "password": "testpass123"
}Execute → should return 201 Created.
Now login:
- Expand POST /api/token/ → Try it out → Enter username & password.
Execute → copy the access token from the response.
Paste it into the Authorize popup as:
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (your full token)
Click Authorize → Close.

2. Browse & Search Books (No Login Needed)
- Expand GET /api/books/
Click Try it out
(Optional) Add query parameters:
search: e.g. "Things Fall Apart"
ordering: e.g. "-title" (descending)

Execute → see paginated list of books with details.

Create a Reservation (Requires Login)
- Expand POST /api/reservations/
Click Try it out
In the request body:JSON{
  "book_id": 1
}(Use any valid book ID from the GET /api/books/ response)
Execute → should return 201 Created with status "reserved" (if copies available) or "queued" (if not).

3. View Your Reservations
- Expand GET /api/reservations/
Try it out → Execute
See your active reservations (reserved or queued).

4. Cancel a Reservation
- Expand POST /api/reservations/{id}/cancel/
Enter the reservation ID from step 5
Try it out → Execute
Should return 200 OK with success message
Check GET /api/reservations/ again → status should be "cancelled"

## Project Structure
  - library_reservation_and_catalog_system/
  - ├── books/                  # Book and Category models, serializers, views
  - ├── reservations/           # Reservation model with queue logic
  - ├── users/
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
    - POST /api/register/ – allows new users to create accounts (username, email, password)

## Sample Data
The admin panel is pre-seeded with real books (e.g., Things Fall Apart, Beneath the Lion's Gaze, Sapiens) across categories like Fiction, African Literature, and Non-Fiction for easy testing.

## Screenshots
![Swagger UI](screenshots/swagger_UI.png)
*Interactive API docs via Swagger*

![Admin Panel](screenshots/admin-books.png)
*Django admin managing books*


## License
MIT License – free to use, modify, and distribute.

## Author
Abdulmenan Amin
ALX Africa Back-End Development Student
