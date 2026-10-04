import pytest

from app import create_app, db


@pytest.fixture
def app():

    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():

        db.create_all()

        yield app

        db.drop_all()


@pytest.fixture
def client(app):

    return app.test_client()


def test_homepage(client):

    response = client.get("/")

    assert response.status_code == 200


def test_health_check(client):

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


def test_create_employee(client):

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


def test_get_employees(client):

    response = client.get(
        "/api/employees"
    )

    assert response.status_code == 200


def test_create_employee_without_email(client):

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