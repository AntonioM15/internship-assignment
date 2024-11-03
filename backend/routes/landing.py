from flask import Blueprint, jsonify, request

# Blueprint definition
landing_blueprint = Blueprint('landing_blueprint', __name__)


# TODO remove example endpoint
@landing_blueprint.route('/message', methods=["GET"])
def create_task():
    return jsonify('Hola mundo desde Flask')


@landing_blueprint.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"status": "error", "message": "Email o contraseña no proporcionado"}), 400

    # TODO mocked response until DB is configured
    if email != 'aa' or password != 'bb':
        return jsonify({"status": "error", "message": "Email o contraseña incorrectos"}), 401

    return jsonify({"status": "success"}), 200


@landing_blueprint.route('/password-recovery', methods=["POST"])
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


@landing_blueprint.route('/contact', methods=["GET"])
def provide_contact():
    # TODO
    return jsonify({"status": "success"}), 200
