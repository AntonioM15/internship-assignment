from flask import Blueprint, jsonify

# Blueprint definition
landing_blueprint = Blueprint('landing_blueprint', __name__)


# TODO remove example endpoint
@landing_blueprint.route('/message', methods=["GET"])
def create_task():
    return jsonify('Hola mundo desde Flask')
