from flask import Blueprint, jsonify
from collections import defaultdict

from backend.generic.models.users import USER_MAPPING
from backend.generic.models.utils import serialize_document

# Blueprint definition
dashboard = Blueprint('dashboard_blueprint', __name__)


def dashboard_blueprint(mongo):
    mongo_db = mongo.db

    @dashboard.route('/', methods=["GET"])
    def get_notifications():
        # TODO save logged user in flask session
        user = {
            'id': '67449aa50871c949f24692cb',
            'role': 'worker'
        }

        # Retrieve notifications
        klass = USER_MAPPING.get(user.get('role'))
        notifications = klass.retrieve_latest_notifications(mongo_db, user.get('id'))

        # Arrange them by role
        response = defaultdict(list)
        for doc in notifications:
            response[doc["role"]].append(serialize_document(doc))

        return jsonify({"status": "success", "message": "Notifications retrieved successfully", "data": response}), 200

    return dashboard
