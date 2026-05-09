# Flask RBAC Application with Admin Panel and REST API

A complete Role-Based Access Control (RBAC) web application built with Flask, featuring user authentication, student management CRUD operations, admin panel, and RESTful API.

## 🚀 Features

### 🔐 Authentication & Authorization
- User registration with password hashing
- Secure login/logout with session management
- Role-based access control (Admin & User roles)
- Protected routes with custom decorators
- Password encryption using Werkzeug

### 👥 User Roles
- **Admin**: Full system access, user management, delete students
- **User**: View students, add students, edit students

### 📚 Student Management (CRUD)
- **Create**: Add new students
- **Read**: View all students
- **Update**: Edit student information
- **Delete**: Remove students (Admin only)

### 🛡️ Admin Panel
- View all registered users
- View complete student list
- Delete any student record
- System statistics dashboard

### 🌐 REST API
- **GET** `/api/students` - Fetch all students
- **POST** `/api/students` - Add new student
- **PUT** `/api/students/<id>` - Update student
- **DELETE** `/api/students/<id>` - Delete student
- JSON response format with proper error handling

### 🎨 Frontend
- Modern responsive design
- Professional gradient background
- Interactive cards and buttons
- Flash messages for user feedback
- Mobile-friendly layout

## 🛠️ Technologies Used

- **Backend**: Python 3, Flask
- **Database**: SQLite3
- **Security**: Werkzeug (password hashing)
- **Frontend**: HTML5, CSS3
- **Authentication**: Session-based
- **API**: RESTful JSON endpoints

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## 🔧 Installation & Setup

### 1. Clone or Download Project
```bash
# Create project directory
mkdir flask_rbac_project
cd flask_rbac_project
