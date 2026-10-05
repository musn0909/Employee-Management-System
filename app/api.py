from flask import Blueprint, request, jsonify
import re

from app import db
from app.models import Employee
from app.auth_utils import login_required, role_required


api = Blueprint("api", __name__)


# --------------------------------------------------
# TEST ENDPOINT
# --------------------------------------------------

@api.route("/test", methods=["GET"])
def test_api():
    return {
        "message": "Employee API is working!"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Employee Management API"
    })


# --------------------------------------------------
# GET ALL EMPLOYEES
# --------------------------------------------------

@api.route("/employees", methods=["GET"])
@login_required
def get_employees():

    employees = Employee.query.all()

    return jsonify([
        employee.to_dict()
        for employee in employees
    ])


# --------------------------------------------------
# CREATE EMPLOYEE
# --------------------------------------------------

@api.route("/employees", methods=["POST"])
@login_required
@role_required("admin", "hr")
def create_employee():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    required_fields = [
        "name",
        "email",
        "department",
        "position",
        "salary"
    ]

    # Check required fields
    for field in required_fields:

        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    # Clean string values
    name = str(data["name"]).strip()
    email = str(data["email"]).strip().lower()
    department = str(data["department"]).strip()
    position = str(data["position"]).strip()

    # Check empty strings
    if not name or not email or not department or not position:

        return jsonify({
            "error": "Name, email, department and position cannot be empty"
        }), 400

    # Validate email
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_pattern, email):

        return jsonify({
            "error": "Invalid email address"
        }), 400

    # Check duplicate email
    existing_employee = Employee.query.filter_by(
        email=email
    ).first()

    if existing_employee:

        return jsonify({
            "error": "Email already exists"
        }), 409

    # Validate salary
    try:

        salary = float(data["salary"])

        if salary < 0:
            raise ValueError

    except (ValueError, TypeError):

        return jsonify({
            "error": "Salary must be a non-negative number"
        }), 400

    # Create employee
    employee = Employee(
        name=name,
        email=email,
        department=department,
        position=position,
        salary=salary
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee created successfully",
        "employee": employee.to_dict()
    }), 201


# --------------------------------------------------
# GET SINGLE EMPLOYEE
# --------------------------------------------------

@api.route("/employees/<int:employee_id>", methods=["GET"])
@login_required
def get_employee(employee_id):

    employee = db.session.get(
        Employee,
        employee_id
    )

    if not employee:

        return jsonify({
            "error": "Employee not found"
        }), 404

    return jsonify(
        employee.to_dict()
    )


# --------------------------------------------------
# UPDATE EMPLOYEE
# --------------------------------------------------

@api.route(
    "/employees/<int:employee_id>",
    methods=["PUT"]
)
@login_required
@role_required("admin", "hr")
def update_employee(employee_id):

    employee = db.session.get(
        Employee,
        employee_id
    )

    if not employee:

        return jsonify({
            "error": "Employee not found"
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    # -------------------------
    # NAME
    # -------------------------

    if "name" in data:

        name = str(data["name"]).strip()

        if not name:

            return jsonify({
                "error": "Name cannot be empty"
            }), 400

        employee.name = name

    # -------------------------
    # EMAIL
    # -------------------------

    if "email" in data:

        email = str(data["email"]).strip().lower()

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_pattern, email):

            return jsonify({
                "error": "Invalid email address"
            }), 400

        # Check whether another employee
        # already uses this email
        existing_employee = Employee.query.filter(
            Employee.email == email,
            Employee.id != employee.id
        ).first()

        if existing_employee:

            return jsonify({
                "error": "Email already exists"
            }), 409

        employee.email = email

    # -------------------------
    # DEPARTMENT
    # -------------------------

    if "department" in data:

        department = str(
            data["department"]
        ).strip()

        if not department:

            return jsonify({
                "error": "Department cannot be empty"
            }), 400

        employee.department = department

    # -------------------------
    # POSITION
    # -------------------------

    if "position" in data:

        position = str(
            data["position"]
        ).strip()

        if not position:

            return jsonify({
                "error": "Position cannot be empty"
            }), 400

        employee.position = position

    # -------------------------
    # SALARY
    # -------------------------

    if "salary" in data:

        try:

            salary = float(data["salary"])

            if salary < 0:
                raise ValueError

            employee.salary = salary

        except (ValueError, TypeError):

            return jsonify({
                "error": "Salary must be a non-negative number"
            }), 400

    # Save changes
    db.session.commit()

    return jsonify({
        "message": "Employee updated successfully",
        "employee": employee.to_dict()
    })


# --------------------------------------------------
# DELETE EMPLOYEE
# --------------------------------------------------

@api.route(
    "/employees/<int:employee_id>",
    methods=["DELETE"]
)
@login_required
@role_required("admin", "hr")
def delete_employee(employee_id):

    employee = db.session.get(
        Employee,
        employee_id
    )

    if not employee:

        return jsonify({
            "error": "Employee not found"
        }), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee deleted successfully"
    })