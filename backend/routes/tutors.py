from bson import ObjectId
from flask import Blueprint, jsonify, request

from generic.models.users import Tutor
from generic.models.utils import serialize_document, Observation

# Blueprint definition
tutors = Blueprint('tutors_blueprint', __name__)


def tutors_blueprint(mongo):
    mongo_db = mongo.db

    @tutors.route('/', methods=["GET"])
    def get_tutors():
        degree_id = request.args.get('degree_id')
        full_name = request.args.get('full_name')
        status = request.args.get('status')

        # Retrieve tutors
        tutor_list = Tutor.retrieve_tutors(mongo_db, degree_id, full_name, status)
        response = {'tutors': [serialize_document(tutor) for tutor in tutor_list]}

        return jsonify({"status": "success", "message": "Tutors retrieved successfully", "data": response}), 200

    @tutors.route('/add', methods=["POST"])
    def add_tutor():
        data = request.get_json()

        email = data.get('email')
        hashed_password = data.get('hashed_password')

        official_id = data.get('official_id')
        full_name = data.get('full_name')
        degree_id = data.get('degree_id')

        # Add new tutor
        tutor = Tutor(email, hashed_password, official_id, full_name, status=None, institution=None,
                      degrees=[ObjectId(degree_id)])
        tutor_doc = tutor.save(mongo_db)

        observation_text = data.get('observation')
        if observation_text:
            # Add new observation and assign it to the tutor
            observation = Observation(text=observation_text, receiver=ObjectId(tutor_doc.inserted_id))
            observation_doc = observation.save(mongo_db)

            # Update tutor
            tutor.update_tutor(mongo_db, tutor_doc.inserted_id,
                               {'observations': [ObjectId(observation_doc.inserted_id)]})

        return jsonify({"message": "Added new tutor"}), 201

    @tutors.route('/update', methods=["PUT"])
    def update_tutor():
        data = request.get_json()
        user_id = data.get('user_id')
        # Dict with the fields and values to update
        data_to_update = data.get('data_to_update')

        # Update tutor
        Tutor.update_tutor(mongo_db, ObjectId(user_id), data_to_update)

        return jsonify({"message": "Tutor was updated"}), 200

    @tutors.route('/hide', methods=["PUT"])
    def hide_tutor():
        data = request.get_json()
        user_id = data.get('user_id')

        # Update tutor
        Tutor.update_tutor(mongo_db, ObjectId(user_id),
                           {'hidden': True})

        return jsonify({"message": "Tutor was hid"}), 200

    @tutors.route('/restore', methods=["PUT"])
    def restore_tutor():
        data = request.get_json()
        user_id = data.get('user_id')

        # Update tutor
        Tutor.update_tutor(mongo_db, ObjectId(user_id),
                           {'hidden': False})

        return jsonify({"message": "Tutor was restored"}), 200

    return tutors
