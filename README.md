# 📔 DayScript - Personal Diary Application

A Django-based personal diary/journal web application for the Web Engineering course project.

## 📋 Project Information

- **Course:** Web Engineering
- **Project Type:** Complex Computing Project - Django Web Application
- **Application:** Personal Diary / Journal

## ✨ Features

### Core Features
- ✅ User Registration and Login (Django built-in authentication)
- ✅ Create, Read, Update, Delete (CRUD) diary entries
- ✅ Mood tracking with emoji indicators
- ✅ Tag-based organization
- ✅ Search functionality (by title and content)
- ✅ Filter by mood, date range, and tags
- ✅ User profile with statistics
- ✅ Admin interface for data management

### Optional Enhancements
- ✅ Advanced filtering (mood, date range, tags)
- ✅ Search functionality
- ✅ Responsive UI/UX design
- ✅ Pagination for entries

## 🛠️ Technology Stack

- **Backend:** Django 5.x
- **Database:** SQLite (default)
- **Frontend:** HTML5, CSS3
- **Authentication:** Django built-in auth system

## 📁 Project Structure

```
dayscript/
├── dayscript/           # Project settings
│   ├── settings.py
│   ├── urls. py
│   └── wsgi.py
├── diary/               # Main application
│   ├── migrations/
│   ├── templates/diary/
│   ├── admin.py
│   ├── forms.py
│   ├── models. py
│   ├── urls.py
│   └── views.py
├── static/css/
│   └── style.css
├── templates/
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation Steps

1. **Extract the project folder**
   ```bash
   unzip dayscript. zip
   cd dayscript
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv . venv
   . venv\Scripts\Activate   # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel:  http://127.0.0.1:8000/admin/

## 📍 URL Endpoints

| URL | Description |
|-----|-------------|
| `/` | Home page / Dashboard |
| `/register/` | User registration |
| `/login/` | User login |
| `/logout/` | User logout |
| `/entry/new/` | Create new diary entry |
| `/entry/<id>/` | View entry details |
| `/entry/<id>/edit/` | Edit entry |
| `/entry/<id>/delete/` | Delete entry |
| `/profile/` | User profile & statistics |
| `/admin/` | Django admin interface |

## 📸 Screenshots

### Home Page
- Displays all diary entries with search and filter options
- Shows mood emoji and content preview

### Create/Edit Entry
- Form with title, content, mood selection
- Tag management (existing and new tags)

### Profile Page
- User statistics (total entries, mood distribution)
- List of used tags

### Admin Interface
- Full CRUD operations for entries and tags
- User management

## 👤 Default Admin Credentials

- **Username:** admin
- **Password:** admin123

## 📝 Models

### DiaryEntry
- `user` - Foreign key to User
- `title` - Entry title (max 200 chars)
- `content` - Entry content (text)
- `mood` - Mood selection (8 options with emojis)
- `tags` - Many-to-many relationship with Tag
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Tag
- `name` - Tag name (unique, max 50 chars)
- `created_at` - Creation timestamp

## 🎨 UI Features

- Modern, responsive design
- Purple/lavender color scheme
- Mobile-friendly layout
- Emoji mood indicators
- Card-based entry display

## 📄 License

This project is created for educational purposes as part of the Web Engineering course. 

---

**Developed by:** Junaid , Shayan and Arif 
**Course:** Web Engineering  
**Date:** December 2025
