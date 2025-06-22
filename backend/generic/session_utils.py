from flask import session, jsonify
from functools import wraps


def login_required(function):
    """ Decorator. Block non-logged users from accessing the resource """
    @wraps(function)
    def _decorator(*args, **kwargs):
        if 'email' not in session:
            return jsonify({"status": "error", "message": "Usuario no autorizado. Por favor, inicie sesión."}), 401

        return function(*args, **kwargs)
    return _decorator


def limited_access(roles):
    """ Decorator. Block users with a non-valid role from accessing the resource

        :param roles: List of allowed roles
    """
    def _decorator_with_params(function):
        @wraps(function)
        def _decorator(*args, **kwargs):
            role = session.get('role')
            if role not in roles:
                return jsonify({"status": "error", "message": "Usuario no autorizado. Página restringida."}), 403

            return function(*args, **kwargs)

        return _decorator
    return _decorator_with_params


def save_session(email, role):
    """ Save user session """
    session['email'] = email
    session['role'] = role


def clear_session():
    """ Clear user session """
    session.clear()
