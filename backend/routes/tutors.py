from flask import Blueprint, jsonify, request
import csv
import io

from generic.models.institutions import Degree
from generic.models.users import Tutor
from generic.models.utils import Observation, serialize_document, to_object_id
from generic.session_utils import limited_access, login_required

# Blueprint definition
tutors = Blueprint('tutors_blueprint', __name__)

# TMP - Default password - to be changed by the final user
DEFAULT_PASSWORD = '1234'


def tutors_blueprint(mongo):
    mongo_db = mongo.db

    @tutors.route('/', methods=["GET"])
    @login_required
    @limited_access(['admin', 'coordinator'])
    def get_tutors():
        degree_id = request.args.get('degree_id')
        full_name = request.args.get('full_name')
        status = request.args.get('status')

        # Retrieve tutors
        tutor_list = Tutor.retrieve_tutors(mongo_db, degree_id, full_name, status, partial_search=True)
        response = {'tutors': [Tutor.doc_to_dict(mongo_db, tutor) for tutor in tutor_list]}

        # Extend response with extra data
        degree_list = Degree.get_latest(mongo_db)
        response['degrees'] = [serialize_document(degree) for degree in degree_list]

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
                      degrees=[degree_id])
        tutor_doc = tutor.save(mongo_db)

        observation_text = data.get('observation')
        if observation_text:
            # Add new observation and assign it to the tutor
            observation = Observation(text=observation_text, receiver=tutor_doc.inserted_id)
            observation_doc = observation.save(mongo_db)

            # Update tutor
            tutor.update_tutor(mongo_db, tutor_doc.inserted_id,
                               {'observations': [to_object_id(observation_doc.inserted_id)]})

        return jsonify({"message": "Added new tutor"}), 201

    @tutors.route('/add-tutors-csv', methods=["POST"])
    def add_tutors_csv():
        """ Given a CSV file included in the request, add new tutors to the database. """
        file = request.files.get('file')
        if not file:
            return jsonify({"message": "Archivo no recibido, abortando creación de profesores"}), 400

        try:
            data_bytes = file.read()
            if not data_bytes:
                return jsonify({"message": "El archivo está vacío"}), 400

            text = data_bytes.decode('utf-8-sig', errors='replace')
            reader = csv.DictReader(io.StringIO(text))

            new_tutors = 0
            errors = []
            for idx, row in enumerate(reader, start=2):  # skip header row
                try:
                    official_id = (row.get('official_id') or '').strip() or None
                    full_name = (row.get('full_name') or '').strip() or None
                    email = (row.get('email') or '').strip() or None
                    degree_codes = (row.get('degrees') or '').strip().replace(' ', '').split(';') or []
                    description = (row.get('description') or '').strip() or None

                    # Retrieve the degree id based on the degree code
                    degrees = Degree.get_multi_by_codes(mongo_db, degree_codes)
                    degree_ids = [degree.get("_id") for degree in degrees if degree]

                    # Minimum checks
                    if not email or not full_name or not official_id:
                        raise ValueError("Faltan campos obligatorios: email, full_name u official_id")

                    # Add the new tutor
                    tutor = Tutor(email, DEFAULT_PASSWORD, official_id, full_name, status=None, institution=None,
                                      degrees=degree_ids, description=description)
                    tutor.save(mongo_db)
                    new_tutors += 1

                except Exception as e:
                    errors.append(f"Fila {idx}: {str(e)}")

            message = f"Added new students: {new_tutors}"
            resp = {"message": message, "created": new_tutors}
            if errors:
                resp["errors"] = errors
                return jsonify(resp), 200

            return jsonify(resp), 201
        except Exception as e:
            return jsonify({"message": f"Error procesando el CSV: {str(e)}"}), 400

    @tutors.route('/update', methods=["PUT"])
    def update_tutor():
        data = request.get_json()
        user_id = data.get('user_id')
        # Dict with the fields and values to update
        data_to_update = data.get('data_to_update')

        # Update tutor
        Tutor.update_tutor(mongo_db, user_id, data_to_update)

        return jsonify({"message": "Tutor was updated"}), 200

    @tutors.route('/hide', methods=["PUT"])
    def hide_tutor():
        data = request.get_json()
        user_id = data.get('user_id')

        # Update tutor
        Tutor.update_tutor(mongo_db, user_id, {'hidden': True})

        return jsonify({"message": "Tutor was hid"}), 200

    @tutors.route('/restore', methods=["PUT"])
    def restore_tutor():
        data = request.get_json()
        user_id = data.get('user_id')

        # Update tutor
        Tutor.update_tutor(mongo_db, user_id, {'hidden': False})

        return jsonify({"message": "Tutor was restored"}), 200

    return tutors
