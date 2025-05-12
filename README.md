# 📝 To-Do Application API

A simple RESTful API built with **Django** and **Django REST Framework** to manage tasks in a To-Do application. This project provides endpoints for creating, reading, updating, and deleting tasks, with optional authentication and filtering features.

## 🚀 Features

- User registration and authentication (optional)
- CRUD operations for to-do tasks
- Task completion status
- API filtering and search (e.g., by status, title)
- Token-based authentication (e.g., JWT or DRF token)
- Admin panel for managing tasks and users

## 🛠️ Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SQLite3 (default DB, can be replaced with PostgreSQL)
- [Optional] Django REST Auth or Simple JWT

1. Create a virtual environment

  python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install dependencies
   
   pip install -r requirements.txt
   
3. Apply migrations

   python manage.py migrate

4. Run the development server

   python manage.py runserver

## API Endpoints

| Method | Endpoint         | Description            |
| ------ | ---------------- | ---------------------- |
| GET    | /api/tasks/      | List all tasks         |
| POST   | /api/tasks/      | Create a new task      |
| GET    | /api/tasks/<id>/ | Retrieve a single task |
| PUT    | /api/tasks/<id>/ | Update a task          |
| DELETE | /api/tasks/<id>/ | Delete a task          |


Your Name - @PrernaSharma



