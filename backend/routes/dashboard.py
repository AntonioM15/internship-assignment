from flask import Blueprint, jsonify
from collections import defaultdict

from generic.models.users import USER_MAPPING
from generic.models.utils import serialize_document
from generic.session_utils import login_required, session_details

# Blueprint definition
dashboard = Blueprint('dashboard_blueprint', __name__)


def dashboard_blueprint(mongo):
    mongo_db = mongo.db

    @dashboard.route('/notifications', methods=["GET"])
    @login_required
    def get_notifications():
        email, role = session_details()
        if not email or not role:
            return jsonify({"status": "error", "message": "Missing user info"}), 401

        # Retrieve notifications
        klass = USER_MAPPING.get(role)
        user = klass.get_by_email(mongo_db, email)
        notifications = klass.retrieve_latest_notifications(mongo_db, user.get('_id', ''))

        # Arrange them by role
        response = defaultdict(list)
        for doc in notifications:
            response[doc["role"]].append(serialize_document(doc))

        return jsonify({"status": "success", "message": "Notifications retrieved successfully", "data": response}), 200

    return dashboard
