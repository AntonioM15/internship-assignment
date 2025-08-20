from bson import ObjectId
from flask import Blueprint, jsonify, request

from generic.models.companies import Company
from generic.models.internships import Internship
from generic.models.utils import serialize_document, str_date_to_datetime
from generic.session_utils import limited_access, login_required

# Blueprint definition
assignments = Blueprint('assignments_blueprint', __name__)


def assignments_blueprint(mongo):
    mongo_db = mongo.db

    @assignments.route('/', methods=["GET"])
    @login_required
    @limited_access(['admin', 'coordinator'])
    def get_assignments():
        student_id = request.args.get('student_id')
        title = request.args.get('title')
        status = request.args.get('status')

        # Retrieve internships
        internship_list = Internship.retrieve_internships(mongo_db, student_id, title, status)
        response = {'internships': [Internship.doc_to_dict(mongo_db, internship) for internship in internship_list]}

        return jsonify({"status": "success", "message": "Internships retrieved successfully", "data": response}), 200

    @assignments.route('/add', methods=["POST"])
    def add_internship():
        data = request.get_json()

        kind = data.get('kind')
        starting_day = str_date_to_datetime(data.get('starting_day'))
        finishing_day = str_date_to_datetime(data.get('finishing_day'))
        title = data.get('title')
        description = data.get('description')
        company_id = data.get('company_id')

        # Add new internship
        internship = Internship(kind, None, starting_day, finishing_day, title, description,
                                company=ObjectId(company_id))
        internship_doc = internship.save(mongo_db)

        # Update company
        Company.add_internship_to_company(mongo_db, ObjectId(company_id), ObjectId(internship_doc.inserted_id))

        return jsonify({"message": "Added new internship"}), 201

    @assignments.route('/update', methods=["PUT"])
    def update_internship():
        data = request.get_json()
        internship_id = data.get('internship_id')
        # Dict with the fields and values to update
        data_to_update = data.get('data_to_update')

        # Update internship
        Internship.update_internship(mongo_db, ObjectId(internship_id), data_to_update)

        return jsonify({"message": "Internship was updated"}), 200

    return assignments
