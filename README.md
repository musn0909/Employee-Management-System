# Employee Management System

A full-stack Employee Management System built with Flask, SQLAlchemy, PostgreSQL, and a REST API.

The application provides employee CRUD operations, authentication, role-based access control, search and filtering, database migrations, automated testing, and cloud deployment.

## Live Demo

**Application:**  
https://employee-management-system-i5go.vercel.app

**GitHub Repository:**  
https://github.com/musn0909/Employee-Management-System

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

### REST API

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

The test suite covers:

- Homepage authentication
- Login
- Logout
- Authentication requirements
- Employee access control
- Admin permissions
- HR permissions
- Viewer restrictions
- Employee creation
- Employee updates
- Employee deletion
- Input validation
- API health check

**Current test status: 16 tests passing**

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
```

---

## Application Structure

### `app/__init__.py`

Implements the Flask application factory.

It initializes:

- Flask
- SQLAlchemy
- Flask-Migrate
- Application blueprints

The application factory also supports configuration overrides, allowing the test suite to use an isolated SQLite database.

### `app/models.py`

Contains the SQLAlchemy database models:

- `Employee`
- `User`

The `User` model stores password hashes rather than plaintext passwords.

### `app/routes.py`

Contains the server-rendered HTML routes for:

- Employee dashboard
- Employee details
- Add employee
- Edit employee
- Delete employee
- Login page

HTML authentication and role-based authorization are enforced here.

### `app/api.py`

Contains the REST API endpoints for employee management.

### `app/auth.py`

Handles authentication endpoints:

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
```

### `app/auth_utils.py`

Contains reusable authentication and authorization decorators.

Examples:

```python
@login_required
```

and:

```python
@role_required("admin", "hr")
```

---

## Authentication Flow

The authentication process works as follows:

```text
User
 │
 ▼
Login Page
 │
 ▼
POST /api/auth/login
 │
 ▼
Find User
 │
 ▼
Verify Password Hash
 │
 ├── Invalid ──► 401 Unauthorized
 │
 └── Valid
       │
       ▼
   Create Session
       │
       ▼
    Dashboard
```

The session stores the authenticated user's:

- User ID
- Username
- Role

---

## Authorization Flow

Employee modification operations require an authenticated user with an appropriate role.

```text
Request
   │
   ▼
Is user logged in?
   │
   ├── No ──► Authentication required
   │
   ▼
Check Role
   │
   ├── Viewer ──► 403 Forbidden
   │
   └── Admin / HR
          │
          ▼
      Perform Action
```

Server-side authorization prevents users from bypassing the frontend by manually accessing protected URLs or API endpoints.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate a user |
| GET | `/api/auth/me` | Get current authenticated user |
| POST | `/api/auth/logout` | Log out the current user |

### Employee API

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/employees` | Authenticated users |
| POST | `/api/employees` | Admin / HR |
| GET | `/api/employees/<id>` | Authenticated users |
| PUT | `/api/employees/<id>` | Admin / HR |
| DELETE | `/api/employees/<id>` | Admin / HR |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | API health check |
| GET | `/api/test` | API test endpoint |

---

## API Examples

### Health Check

```http
GET /api/health
```

Response:

```json
{
    "status": "healthy",
    "service": "Employee Management API"
}
```

### Create Employee

```http
POST /api/employees
Content-Type: application/json
```

Example request:

```json
{
    "name": "Ali Khan",
    "email": "ali@example.com",
    "department": "IT",
    "position": "Python Developer",
    "salary": 75000
}
```

Successful response:

```json
{
    "message": "Employee created successfully",
    "employee": {
        "id": 1,
        "name": "Ali Khan",
        "email": "ali@example.com",
        "department": "IT",
        "position": "Python Developer",
        "salary": 75000
    }
}
```

---

## Database Schema

### Users

```text
users
├── id
├── username
├── email
├── password_hash
├── role
└── created_at
```

### Employees

```text
employees
├── id
├── name
├── email
├── department
├── position
└── salary
```

---

## Database Migrations

The project uses Flask-Migrate and Alembic to manage database schema changes.

Create a migration:

```powershell
flask db migrate -m "Describe the change"
```

Apply migrations:

```powershell
flask db upgrade
```

---

## Local Development

### 1. Clone the repository

```bash
git clone https://github.com/musn0909/Employee-Management-System.git
```

```bash
cd Employee-Management-System
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=your-postgresql-database-url
```

Do not commit `.env` to GitHub.

### 5. Run database migrations

```powershell
flask db upgrade
```

### 6. Start the application

```powershell
python run.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## Running Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

Current result:

```text
16 passed
```

The tests use an isolated in-memory SQLite database, so the production PostgreSQL database is not modified during testing.

---

## Test Users

The following accounts are used by the automated test suite:

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@test.com` | `AdminPass123!` |
| HR | `hr@test.com` | `HRPass123!` |
| Viewer | `viewer@test.com` | `ViewerPass123!` |

These are **test database credentials only** and should not be used as production credentials.

---

## Production Roles

The deployed application uses separate user accounts in the production Neon database.

Production credentials should never be stored in this README or committed to GitHub.

---

## Environment Variables

The application uses environment variables for configuration.

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Flask session security |
| `DATABASE_URL` | PostgreSQL database connection |

Example:

```env
SECRET_KEY=change-this-in-production
DATABASE_URL=postgresql://...
```

---

## Security

The application implements several security practices:

- Passwords are stored using Werkzeug password hashing
- Authentication is required for protected resources
- Role-based authorization is enforced server-side
- Viewer users cannot modify employee records
- Duplicate employee emails are rejected
- Salary values are validated
- Environment secrets are excluded from Git
- Database migrations are managed through Flask-Migrate
- Protected HTML routes redirect unauthenticated users to the login page
- Protected API routes return appropriate authentication/authorization errors

---

## Deployment

The application is deployed using Vercel.

The production application uses:

- Flask
- Gunicorn
- PostgreSQL through Neon
- Environment-based configuration

Production database credentials are stored as environment variables rather than inside the source code.

---

## Future Improvements

Potential future improvements include:

- Pagination
- Advanced employee filtering
- Employee profile photos
- Audit logs
- Password reset
- Email verification
- JWT authentication for external API clients
- Admin user management interface
- Dashboard statistics
- CSV import/export
- Docker containerization
- CI/CD with GitHub Actions

---

## What I Learned

This project was developed as a practical backend and full-stack learning project.

Key concepts implemented include:

- Flask application factory pattern
- REST API development
- SQLAlchemy ORM
- PostgreSQL database integration
- Database migrations with Alembic
- Password hashing
- Session-based authentication
- Role-based access control
- Server-side authorization
- Input validation
- Automated testing with pytest
- Git and GitHub workflow
- Cloud deployment
- Environment-based configuration

---

## Author

### Muhammad Umar Shamas Nasir

**Computer Science Graduate | Backend & Software Development Enthusiast**

Interested in:

- Backend Development
- Python & Flask
- REST APIs
- Database Systems
- Cloud Technologies
- SAP Business Technology Platform (SAP BTP)
- Artificial Intelligence & Machine Learning

### Connect

**GitHub:**  
https://github.com/musn0909

**LinkedIn:**  
Add your LinkedIn profile URL here

---

## License

This project is intended as a portfolio and learning project.