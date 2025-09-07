from flask import session, jsonify, request
from functools import wraps
import logging


logger = logging.getLogger(__name__)

def login_required(function):
    """ Decorator. Block non-logged users from accessing the resource """
    @wraps(function)
    def _decorator(*args, **kwargs):
        if 'email' not in session:
            logger.error(f"Unauthenticated access attempt to {request.path}")
            return jsonify({"status": "error", "message": "Usuario no autorizado. Por favor, inicie sesión."}), 401

        logger.info(f"Authenticated access attempt to {request.path} by user {session.get('email')}")
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
                logger.info(
                    f"Prevented access of role {role} to {request.path} by user {session.get('email')}. "
                    f"Allowed roles are {roles}"
                )
                return jsonify({"status": "error", "message": "Usuario no autorizado. Página restringida."}), 403

            logger.info(f"Access granted to {request.path} by user {session.get('email')}")
            return function(*args, **kwargs)

        return _decorator
    return _decorator_with_params


def save_session(email, role):
    """ Save user session """
    logger.info(f"User {email} with role {role} logged in")
    session['email'] = email
    session['role'] = role


def clear_session():
    """ Clear user session """
    logger.info(f"User {session.get('email')} with role {session.get('role')} logged out")
    session.clear()

def session_details():
    return session.get('email'), session.get('role')
