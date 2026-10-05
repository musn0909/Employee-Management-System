# Employee Management System

A full-stack Employee Management System built with Flask, SQLAlchemy, PostgreSQL, and a REST API. The application provides employee CRUD operations, authentication, role-based access control, search/filtering, database migrations, automated testing, and cloud deployment.

## Live Demo

**Application:** https://employee-management-system-i5go.vercel.app

**GitHub:** https://github.com/musn0909/Employee-Management-System

---

## Features

### Employee Management

- Create employees
- View employee details
- Update employee information
- Delete employees
- Search employees by name
- Filter employees by department
- Salary validation
- Duplicate email validation

### Authentication

- User registration
- User login/logout
- Password hashing
- Session-based authentication
- Current-user endpoint
- Protected application routes
- Protected REST API endpoints

### Role-Based Access Control

The system supports three roles:

| Role | View | Add | Edit | Delete |
|------|------|-----|------|--------|
| Admin | Yes | Yes | Yes | Yes |
| HR | Yes | Yes | Yes | Yes |
| Viewer | Yes | No | No | No |

Authorization is enforced on the server, not only through frontend UI controls.

### API

REST API endpoints are available for:

- Authentication
- Employee listing
- Employee creation
- Employee retrieval
- Employee updates
- Employee deletion
- Health checks

### Database

- PostgreSQL database using Neon
- SQLAlchemy ORM
- Flask-Migrate
- Alembic migrations
- SQLite in-memory database for automated tests

### Testing

The project includes automated tests using `pytest`.

Current test coverage includes:

- Homepage authentication
- Login
- Logout
- Authentication requirements
- Employee access control
- Admin permissions
- HR permissions
- Viewer restrictions
- Employee creation
- Employee update
- Employee deletion
- Validation
- API health check

Current test status:

**16 tests passing**

---

## Technology Stack

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate
- Werkzeug

### Database

- PostgreSQL
- Neon
- SQLite for testing
- Alembic

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2

### Testing

- pytest

### Development & Deployment

- Git
- GitHub
- Vercel
- Gunicorn
- python-dotenv

---

## Project Architecture

```text
Employee Management System
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── api.py
│   ├── auth.py
│   ├── auth_utils.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── add_employee.html
│   │   ├── edit_employee.html
│   │   └── employee_detail.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
│
├── migrations/
│
├── tests/
│   └── test_employee.py
│
├── config.py
├── run.py
├── requirements.txt
├── pytest.ini
├── pyproject.toml
├── .env
├── .gitignore
└── README.md