from bson import ObjectId
from flask import Blueprint, jsonify, request

from generic.models.users import Student
from generic.models.utils import serialize_document, Observation
from generic.session_utils import limited_access, login_required

# Blueprint definition
students = Blueprint('students_blueprint', __name__)


def students_blueprint(mongo):
    mongo_db = mongo.db

    @students.route('/', methods=["GET"])
    @login_required
    @limited_access(['admin', 'coordinator'])
    def get_students():
        degree_id = request.args.get('degree_id')
        full_name = request.args.get('full_name')
        status = request.args.get('status')

        # Retrieve students
        student_list = Student.retrieve_students(mongo_db, degree_id, full_name, status)
        response = {'students': [serialize_document(student) for student in student_list]}

        return jsonify({"status": "success", "message": "Students retrieved successfully", "data": response}), 200

    @students.route('/add', methods=["POST"])
    def add_student():
        data = request.get_json()

        # TODO not included in final version, added them here to make things easier
        email = data.get('email')
        hashed_password = data.get('hashed_password')

        official_id = data.get('official_id')
        full_name = data.get('full_name')
        degree_id = data.get('degree_id')

        # Add new student
        student = Student(email, hashed_password, official_id, full_name, status=None, institution=None,
                          degree=ObjectId(degree_id))
        student_doc = student.save(mongo_db)

        observation_text = data.get('observation')
        if observation_text:
            # Add new observation and assign it to the student
            observation = Observation(text=observation_text, receiver=ObjectId(student_doc.inserted_id))
            observation_doc = observation.save(mongo_db)

            # Update student
            student.update_student(mongo_db, student_doc.inserted_id,
                                   {'observations': [ObjectId(observation_doc.inserted_id)]})

        return jsonify({"message": "Added new student"}), 201

    @students.route('/update', methods=["PUT"])
    def update_student():
        data = request.get_json()
        user_id = data.get('user_id')
        # Dict with the fields and values to update
        data_to_update = data.get('data_to_update')

        # Update student
        Student.update_student(mongo_db, ObjectId(user_id), data_to_update)

        return jsonify({"message": "Student was updated"}), 200

    @students.route('/hide', methods=["PUT"])
    def hide_student():
        data = request.get_json()
        user_id = data.get('user_id')

        # Update student
        Student.update_student(mongo_db, ObjectId(user_id),
                               {'hidden': True})

        return jsonify({"message": "Student was hid"}), 200

    @students.route('/restore', methods=["PUT"])
    def restore_student():
        data = request.get_json()
        user_id = data.get('user_id')

        # Update student
        Student.update_student(mongo_db, ObjectId(user_id),
                               {'hidden': False})

        return jsonify({"message": "Student was restored"}), 200

    return students
