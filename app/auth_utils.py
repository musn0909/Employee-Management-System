from functools import wraps

from flask import jsonify, session


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({
                "error": "Authentication required"
            }), 401

        return view_function(*args, **kwargs)

    return wrapped_view


def role_required(*allowed_roles):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            if "user_id" not in session:
                return jsonify({
                    "error": "Authentication required"
                }), 401

            user_role = session.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "error": "You do not have permission to perform this action"
                }), 403

            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator