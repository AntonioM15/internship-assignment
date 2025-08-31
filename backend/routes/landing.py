from flask import Blueprint, jsonify, request

from generic.session_utils import save_session, clear_session

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

        # TODO mocked response until DB is configured
        if email != 'aa' or password != 'bb':
            return jsonify({"status": "error", "message": "Email o contraseña incorrectos"}), 401

        role = 'admin'
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

        # TODO mocked response until DB is configured
        if email != 'aa':
            return jsonify({"status": "error", "message": "Email incorrecto"}), 401

        # TODO send email to reset credentials
        return jsonify({"status": "success", "message": "Email con instrucciones enviado"}), 200

    @landing.route('/contact', methods=["GET"])
    def provide_contact():
        # TODO
        return jsonify({"status": "success"}), 200

    return landing
