# Advanced Blog Platform - Django

A beautiful, full-featured blog platform built with Django featuring modern UI design inspired by contemporary blog layouts, user authentication, role-based permissions, comments, categories, tags, and advanced search functionality.

## ✨ Features

### Modern UI Design
- **Gradient Hero Section**: Eye-catching hero with search functionality
- **Card-Based Layout**: Beautiful card designs with hover animations
- **Colorful Category Badges**: Vibrant gradient badges for different categories
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Modern Typography**: Inter font family for clean, readable text
- **Smooth Animations**: Elegant transitions and hover effects
- **Newsletter Section**: Integrated email subscription area

### Core Features
- User Authentication (Register/Login/Logout)
- Role-based Permissions (Admin, Author, Reader)
- Create, Edit, Delete Posts (Authors only)
- Rich Text Editor (CKEditor)
- Featured Images for Posts
- Categories and Tags
- Comments System
- Advanced Search
- Pagination
- Responsive Dashboard

## Setup Instructions

### 1. Clone or Download the Project

```bash
cd blog-platform-django
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Create Media and Static Directories

```bash
# Windows
mkdir media
mkdir static
mkdir staticfiles

# Linux/Mac
mkdir -p media static staticfiles
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Test Accounts

Use these pre-created accounts to test the application:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Author | john_author | author123 |
| Author | jane_author | author123 |
| Reader | reader1 | reader123 |

## Access Points

- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Register**: http://127.0.0.1:8000/accounts/register/

## Project Structure

```
blog-platform-django/
├── advanced_blog/          # Main project directory
├── blog/                   # Blog app
├── accounts/               # User management app
├── templates/              # HTML templates
├── static/                 # Static files
├── media/                  # User-uploaded files
├── manage.py
└── requirements.txt
```

## Technologies Used

- **Backend**: Django 5.2.8
- **Frontend**: Bootstrap 5, Custom CSS with gradients
- **Fonts**: Google Fonts (Inter)
- **Icons**: Bootstrap Icons
- **Editor**: CKEditor for rich text editing
- **Database**: SQLite (development)
- **Image Processing**: Pillow

## UI Design Features

The platform features a modern, visually appealing design inspired by contemporary blog platforms:

- **Color Scheme**: 
  - Primary Blue: `#5B72EE`
  - Primary Purple: `#6B5FED`
  - Gradient combinations for visual interest
  
- **Component Library**:
  - Modern card designs with rounded corners (16px)
  - Gradient buttons with hover effects
  - Category-specific color badges
  - Avatar placeholders with initials
  - Smooth page transitions
  
- **Typography**:
  - Font Family: Inter (Google Fonts)
  - Hierarchical heading sizes
  - Optimized line-height for readability

## Screenshots

The UI includes:
- Hero section with gradient background and search
- Card-based post layout with images
- Category pills with icons
- Modern footer with social links
- Clean login/register forms
- Detailed post view with author info
- Comment section with user avatars
