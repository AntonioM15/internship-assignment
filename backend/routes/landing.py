from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from generic.models.users import User
from generic.session_utils import save_session, clear_session, session_details

# Blueprint definition
landing = Blueprint('landing_blueprint', __name__)


def landing_blueprint(mongo):
    mongo_db = mongo.db

    @landing.route('/login', methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"status": "error", "message": "Email o contraseña no proporcionado"}), 400

        user = User.get_by_email(mongo_db, email)
        stored_password = user.get('hashed_password') if user else None
        if not user or not check_password_hash(stored_password, password):
            return jsonify({"status": "error", "message": "Email o contraseña incorrectos"}), 401

        role = user.get('role')
        save_session(email, role)

        return jsonify({"status": "success"}), 200

    @landing.route('/logout', methods=["POST"])
    def logout():
        clear_session()

        return jsonify({"status": "success"}), 200

    @landing.route('/password-recovery', methods=["POST"])
    def recover_password():
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({"status": "error", "message": "Email no proporcionado"}), 400

        user = User.get_by_email(mongo_db, email)
        if not user:
            return jsonify({"status": "error", "message": "Email incorrecto"}), 401

        # TODO send email to reset credentials
        return jsonify({"status": "success", "message": "Email con instrucciones enviado"}), 200

    @landing.route('/contact', methods=["GET"])
    def provide_contact():
        # TODO
        return jsonify({"status": "success"}), 200

    @landing.route('/is-user-logged-in', methods=["GET"])
    def is_user_logged_in():
        email, role = session_details()
        return jsonify({"status": "success", "data": {"logged_in": bool(email and role)}}), 200


    return landing
