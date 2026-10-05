from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app import db
from app.models import Employee


main = Blueprint("main", __name__)


# ---------------------------------------------------------
# HTML Authentication Helpers
# ---------------------------------------------------------

def html_login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("main.login_page"))

        return view_function(*args, **kwargs)

    return wrapped_view


def html_role_required(*allowed_roles):
    def decorator(view_function):

        @wraps(view_function)
        def wrapped_view(*args, **kwargs):

            if "user_id" not in session:
                return redirect(url_for("main.login_page"))

            if session.get("role") not in allowed_roles:
                flash(
                    "You do not have permission to perform this action.",
                    "error"
                )

                return redirect(url_for("main.index"))

            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator


# ---------------------------------------------------------
# Dashboard / Employee List
# ---------------------------------------------------------

@main.route("/")
@html_login_required
def index():

    search = request.args.get("search", "")
    department = request.args.get("department", "")

    query = Employee.query

    # Search by employee name
    if search:
        query = query.filter(
            Employee.name.ilike(f"%{search}%")
        )

    # Filter by department
    if department:
        query = query.filter_by(
            department=department
        )

    employees = query.order_by(
        Employee.id.desc()
    ).all()

    # Get unique departments
    departments = db.session.query(
        Employee.department
    ).distinct().all()

    departments = [
        item[0]
        for item in departments
    ]

    return render_template(
        "index.html",
        employees=employees,
        departments=departments,
        search=search,
        selected_department=department
    )


# ---------------------------------------------------------
# Employee Details
# ---------------------------------------------------------

@main.route("/employee/<int:employee_id>")
@html_login_required
def employee_detail(employee_id):

    employee = Employee.query.get_or_404(
        employee_id
    )

    return render_template(
        "employee_detail.html",
        employee=employee
    )


# ---------------------------------------------------------
# Add Employee
# Admin / HR Only
# ---------------------------------------------------------

@main.route(
    "/employee/add",
    methods=["GET", "POST"]
)
@html_role_required("admin", "hr")
def add_employee():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        department = request.form.get(
            "department",
            ""
        ).strip()

        position = request.form.get(
            "position",
            ""
        ).strip()

        salary = request.form.get(
            "salary",
            ""
        ).strip()

        # Check empty fields
        if not all([
            name,
            email,
            department,
            position,
            salary
        ]):

            flash(
                "All fields are required.",
                "error"
            )

            return redirect(
                url_for("main.add_employee")
            )

        # Validate salary
        try:

            salary = float(salary)

            if salary < 0:
                raise ValueError

        except (ValueError, TypeError):

            flash(
                "Salary must be a valid non-negative number.",
                "error"
            )

            return redirect(
                url_for("main.add_employee")
            )

        # Check duplicate email
        existing_employee = Employee.query.filter_by(
            email=email
        ).first()

        if existing_employee:

            flash(
                "An employee with this email already exists.",
                "error"
            )

            return redirect(
                url_for("main.add_employee")
            )

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

        flash(
            "Employee added successfully!",
            "success"
        )

        return redirect(
            url_for("main.index")
        )

    return render_template(
        "add_employee.html"
    )


# ---------------------------------------------------------
# Edit Employee
# Admin / HR Only
# ---------------------------------------------------------

@main.route(
    "/employee/<int:employee_id>/edit",
    methods=["GET", "POST"]
)
@html_role_required("admin", "hr")
def edit_employee(employee_id):

    employee = Employee.query.get_or_404(
        employee_id
    )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        department = request.form.get(
            "department",
            ""
        ).strip()

        position = request.form.get(
            "position",
            ""
        ).strip()

        salary = request.form.get(
            "salary",
            ""
        ).strip()

        # Validate required fields
        if not all([
            name,
            email,
            department,
            position,
            salary
        ]):

            flash(
                "All fields are required.",
                "error"
            )

            return redirect(
                url_for(
                    "main.edit_employee",
                    employee_id=employee.id
                )
            )

        # Validate salary
        try:

            salary = float(salary)

            if salary < 0:
                raise ValueError

        except (ValueError, TypeError):

            flash(
                "Invalid salary.",
                "error"
            )

            return redirect(
                url_for(
                    "main.edit_employee",
                    employee_id=employee.id
                )
            )

        # Check duplicate email
        duplicate = Employee.query.filter(
            Employee.email == email,
            Employee.id != employee.id
        ).first()

        if duplicate:

            flash(
                "Another employee already uses this email.",
                "error"
            )

            return redirect(
                url_for(
                    "main.edit_employee",
                    employee_id=employee.id
                )
            )

        # Update employee
        employee.name = name
        employee.email = email
        employee.department = department
        employee.position = position
        employee.salary = salary

        db.session.commit()

        flash(
            "Employee updated successfully!",
            "success"
        )

        return redirect(
            url_for(
                "main.employee_detail",
                employee_id=employee.id
            )
        )

    return render_template(
        "edit_employee.html",
        employee=employee
    )


# ---------------------------------------------------------
# Delete Employee
# Admin / HR Only
# ---------------------------------------------------------

@main.route(
    "/employee/<int:employee_id>/delete",
    methods=["POST"]
)
@html_role_required("admin", "hr")
def delete_employee(employee_id):

    employee = Employee.query.get_or_404(
        employee_id
    )

    db.session.delete(employee)
    db.session.commit()

    flash(
        "Employee deleted successfully!",
        "success"
    )

    return redirect(
        url_for("main.index")
    )


# ---------------------------------------------------------
# Login Page
# ---------------------------------------------------------

@main.route("/login")
def login_page():

    if "user_id" in session:
        return redirect(
            url_for("main.index")
        )

    return render_template(
        "login.html"
    )