from flask import Blueprint, jsonify, request
import os

from session_utils import save_session

# Blueprint definition
test_routes = Blueprint('test_routes_blueprint', __name__)


def test_routes_blueprint(mongo):
    mongo_db = mongo.db

    if os.environ.get("TEST_ENV") == "1":
        @test_routes.route('/login-admin', methods=["POST"])
        def login_admin():
            email = request.json.get("email")
            save_session(email, 'admin')

            return jsonify({"status": "success"}), 200

    return test_routes
