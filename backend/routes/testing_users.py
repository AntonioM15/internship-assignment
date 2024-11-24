from flask import Blueprint, request, jsonify

testing_users = Blueprint('testing_users', __name__)


def testing_users_blueprint(mongo):
    mongo_db = mongo.db

    @testing_users.route('/', methods=['POST'])
    def add_user():
        data = request.json
        mongo_db.testing_users.insert_one(data)
        return jsonify({"message": "Added new user"}), 201

    @testing_users.route('/', methods=['GET'])
    def get_user():
        users = mongo_db.testing_users.find()
        result = [{key: user[key] for key in user if key != '_id'} for user in users]
        return jsonify(result), 200

    return testing_users
