import pytest

from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        db.create_all()

        admin = User(
            username="admin",
            email="admin@test.com",
            role="admin"
        )
        admin.set_password("AdminPass123!")

        viewer = User(
            username="viewer",
            email="viewer@test.com",
            role="viewer"
        )
        viewer.set_password("ViewerPass123!")

        db.session.add_all([admin, viewer])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, email, password):
    return client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password
        }
    )


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200


def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


def test_login(client):
    response = login(
        client,
        "admin@test.com",
        "AdminPass123!"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["user"]["role"] == "admin"


def test_me_requires_login(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401


def test_unauthenticated_employee_access(client):
    response = client.get("/api/employees")

    assert response.status_code == 401


def test_viewer_can_get_employees(client):
    login(
        client,
        "viewer@test.com",
        "ViewerPass123!"
    )

    response = client.get("/api/employees")

    assert response.status_code == 200


def test_viewer_cannot_create_employee(client):
    login(
        client,
        "viewer@test.com",
        "ViewerPass123!"
    )

    response = client.post(
        "/api/employees",
        json={
            "name": "Ali Khan",
            "email": "ali@example.com",
            "department": "IT",
            "position": "Python Developer",
            "salary": 75000
        }
    )

    assert response.status_code == 403


def test_admin_can_create_employee(client):
    login(
        client,
        "admin@test.com",
        "AdminPass123!"
    )

    response = client.post(
        "/api/employees",
        json={
            "name": "Ali Khan",
            "email": "ali@example.com",
            "department": "IT",
            "position": "Python Developer",
            "salary": 75000
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["employee"]["name"] == "Ali Khan"


def test_create_employee_without_email(client):
    login(
        client,
        "admin@test.com",
        "AdminPass123!"
    )

    response = client.post(
        "/api/employees",
        json={
            "name": "Ahmed",
            "department": "HR",
            "position": "HR Officer",
            "salary": 65000
        }
    )

    assert response.status_code == 400


def test_admin_can_update_employee(client):
    login(
        client,
        "admin@test.com",
        "AdminPass123!"
    )

    create_response = client.post(
        "/api/employees",
        json={
            "name": "Old Name",
            "email": "update@example.com",
            "department": "IT",
            "position": "Developer",
            "salary": 60000
        }
    )

    assert create_response.status_code == 201

    employee_id = create_response.get_json()["employee"]["id"]

    response = client.put(
        f"/api/employees/{employee_id}",
        json={
            "name": "Updated Name",
            "salary": 70000
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["employee"]["name"] == "Updated Name"
    assert data["employee"]["salary"] == 70000


def test_viewer_cannot_update_employee(client):
    login(
        client,
        "viewer@test.com",
        "ViewerPass123!"
    )

    response = client.put(
        "/api/employees/1",
        json={
            "name": "Hacked Name"
        }
    )

    assert response.status_code == 403


def test_admin_can_delete_employee(client):
    login(
        client,
        "admin@test.com",
        "AdminPass123!"
    )

    create_response = client.post(
        "/api/employees",
        json={
            "name": "Delete Me",
            "email": "delete@example.com",
            "department": "HR",
            "position": "Officer",
            "salary": 50000
        }
    )

    assert create_response.status_code == 201

    employee_id = create_response.get_json()["employee"]["id"]

    response = client.delete(
        f"/api/employees/{employee_id}"
    )

    assert response.status_code == 200


def test_viewer_cannot_delete_employee(client):
    login(
        client,
        "viewer@test.com",
        "ViewerPass123!"
    )

    response = client.delete(
        "/api/employees/1"
    )

    assert response.status_code == 403


def test_logout(client):
    login(
        client,
        "admin@test.com",
        "AdminPass123!"
    )

    response = client.post("/api/auth/logout")

    assert response.status_code == 200

    response = client.get("/api/auth/me")

    assert response.status_code == 401