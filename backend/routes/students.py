from flask import Blueprint, jsonify, request
import csv
import io

from generic.models.institutions import Degree
from generic.models.users import Student
from generic.models.utils import Observation, serialize_document, to_object_id
from generic.session_utils import limited_access, login_required

# Blueprint definition
students = Blueprint('students_blueprint', __name__)

# TMP - Default password - to be changed by the final user
DEFAULT_PASSWORD = '1234'


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
        student_list = Student.retrieve_students(mongo_db, degree_id, full_name, status, partial_search=True)
        response = {'students': [Student.doc_to_dict(mongo_db, student) for student in student_list]}

        # Extend response with extra data
        degree_list = Degree.get_latest(mongo_db)
        response['degrees'] = [serialize_document(degree) for degree in degree_list]

        return jsonify({"status": "success", "message": "Students retrieved successfully", "data": response}), 200

    @students.route('/add', methods=["POST"])
    def add_student():
        data = request.get_json()
        email = data.get('email')
        hashed_password = data.get('hashed_password')
        official_id = data.get('official_id')
        full_name = data.get('full_name')
        degree_id = data.get('degree_id')

        # Add new student
        student = Student(email, hashed_password, official_id, full_name, status=None, institution=None,
                          degree=degree_id)
        student_doc = student.save(mongo_db)

        observation_text = data.get('observation')
        if observation_text:
            # Add new observation and assign it to the student
            observation = Observation(text=observation_text, receiver=student_doc.inserted_id)
            observation_doc = observation.save(mongo_db)

            # Update student
            student.update_student(mongo_db, student_doc.inserted_id,
                                   {'observations': [to_object_id(observation_doc.inserted_id)]})

        return jsonify({"message": "Added new student"}), 201

    @students.route('/add-students-csv', methods=["POST"])
    def add_students_csv():
        """ Given a CSV file included in the request, add new students to the database. """
        file = request.files.get('file')
        if not file:
            return jsonify({"message": "Archivo no recibido, abortando creación de estudiantes"}), 400

        try:
            data_bytes = file.read()
            if not data_bytes:
                return jsonify({"message": "El archivo está vacío"}), 400

            text = data_bytes.decode('utf-8-sig', errors='replace')
            reader = csv.DictReader(io.StringIO(text))

            new_students = 0
            errors = []
            for idx, row in enumerate(reader, start=2):  # skip header row
                try:
                    official_id = (row.get('official_id') or '').strip() or None
                    full_name = (row.get('full_name') or '').strip() or None
                    email = (row.get('email') or '').strip() or None
                    degree_code = (row.get('degree') or '').strip() or None
                    internship_type = (row.get('internship_type') or '').strip() or None
                    description = (row.get('description') or '').strip() or None

                    # Retrieve the degree id based on the degree code
                    degree = Degree.get_by_code(mongo_db, degree_code)
                    degree_id = degree.get("_id") if degree else None

                    # Minimum checks
                    if not email or not full_name or not official_id:
                        raise ValueError("Faltan campos obligatorios: email, full_name u official_id")

                    # Add the new student
                    student = Student(email, DEFAULT_PASSWORD, official_id, full_name, status=None, institution=None,
                                      degree=degree_id, description=description, internship_type=internship_type)
                    student.save(mongo_db)
                    new_students += 1

                except Exception as e:
                    errors.append(f"Fila {idx}: {str(e)}")

            message = f"Added new students: {new_students}"
            resp = {"message": message, "created": new_students}
            if errors:
                resp["errors"] = errors
                return jsonify(resp), 200

            return jsonify(resp), 201
        except Exception as e:
            return jsonify({"message": f"Error procesando el CSV: {str(e)}"}), 400

    @students.route('/update', methods=["PUT"])
    def update_student():
        data = request.get_json()
        user_id = data.get('user_id')
        # Dict with the fields and values to update
        data_to_update = data.get('data_to_update')

        # Update student
        Student.update_student(mongo_db, user_id, data_to_update)

        return jsonify({"message": "Student was updated"}), 200

    @students.route('/hide', methods=["PUT"])
    def hide_student():
        data = request.get_json()
        user_id = data.get('user_id')

        # Update student
        Student.update_student(mongo_db, user_id, {'hidden': True})

        return jsonify({"message": "Student was hid"}), 200

    @students.route('/restore', methods=["PUT"])
    def restore_student():
        data = request.get_json()
        user_id = data.get('user_id')

        # Update student
        Student.update_student(mongo_db, user_id, {'hidden': False})

        return jsonify({"message": "Student was restored"}), 200

    return students
