from flask import Blueprint, jsonify, request
import csv
import io

from generic.models.institutions import Degree
from generic.models.companies import Company
from generic.models.utils import serialize_document, Observation, AVAILABLE_STATUSES, to_object_id
from generic.session_utils import limited_access, login_required

# Blueprint definition
companies = Blueprint('companies_blueprint', __name__)


def companies_blueprint(mongo):
    mongo_db = mongo.db

    @companies.route('/', methods=["GET"])
    @login_required
    @limited_access(['admin', 'coordinator'])
    def get_companies():
        field = request.args.get('field')
        full_name = request.args.get('full_name')
        status = request.args.get('status')

        if not status or status not in AVAILABLE_STATUSES:
            status = None

        # Retrieve companies
        response = {'companies': []}
        company_list = Company.retrieve_companies(mongo_db, field, full_name, partial_search=True)

        # Filter internships
        for company in company_list:
            company_json = Company.doc_to_dict(mongo_db, company)
            internships = company_json.get('internships', [])
            if not internships and status:
                # We are filtering by status and the company doesn't have a matching internship
                continue
            # Only include internships with matching status
            internships_to_display = [internship for internship in internships
                                      if not status or internship.get('status') == status]
            company_json['internships'] = internships_to_display
            response['companies'].append(company_json)

        # Extend response with extra data
        degree_list = Degree.get_latest(mongo_db)
        response['degrees'] = [serialize_document(degree) for degree in degree_list]

        return jsonify({"status": "success", "message": "Companies retrieved successfully", "data": response}), 200

    @companies.route('/add', methods=["POST"])
    def add_company():
        data = request.get_json()

        full_name = data.get('full_name')
        field = data.get('field')

        # Add new company
        company = Company(full_name, field)
        company_doc = company.save(mongo_db)

        observation_text = data.get('observation')
        if observation_text:
            # Add new observation and assign it to the company
            observation = Observation(text=observation_text, receiver=company_doc.inserted_id)
            observation_doc = observation.save(mongo_db)

            # Update company
            company.update_company(mongo_db, company_doc.inserted_id,
                                   {'observations': [to_object_id(observation_doc.inserted_id)]})

        return jsonify({"message": "Added new company"}), 201

    @companies.route('/add-companies-csv', methods=["POST"])
    def add_tutors_csv():
        """ Given a CSV file included in the request, add new companies to the database. """
        file = request.files.get('file')
        if not file:
            return jsonify({"message": "Archivo no recibido, abortando creación de empresas"}), 400

        try:
            data_bytes = file.read()
            if not data_bytes:
                return jsonify({"message": "El archivo está vacío"}), 400

            text = data_bytes.decode('utf-8-sig', errors='replace')
            reader = csv.DictReader(io.StringIO(text))

            new_companies = 0
            errors = []
            for idx, row in enumerate(reader, start=2):  # skip header row
                try:
                    full_name = (row.get('full_name') or '').strip() or None
                    field = (row.get('field') or '').strip() or None
                    description = (row.get('description') or '').strip() or None

                    # Retrieve the degree id based on the field name
                    degree = Degree.get_by_name(mongo_db, field)
                    degree_id = degree.get("_id") if degree else None

                    # Minimum checks
                    if not full_name:
                        raise ValueError("Faltan campos obligatorios: full_name")
                    if not degree_id:
                        raise ValueError(f"No se han grados asociados al campo {field}")

                    # Add the new tutor
                    company = Company(full_name, field, description=description)
                    company.save(mongo_db)
                    new_companies += 1

                except Exception as e:
                    errors.append(f"Fila {idx}: {str(e)}")

            message = f"Added new students: {new_companies}"
            resp = {"message": message, "created": new_companies}
            if errors:
                resp["errors"] = errors
                return jsonify(resp), 200

            return jsonify(resp), 201
        except Exception as e:
            return jsonify({"message": f"Error procesando el CSV: {str(e)}"}), 400

    @companies.route('/update', methods=["PUT"])
    def update_company():
        data = request.get_json()
        company_id = data.get('company_id')
        # Dict with the fields and values to update
        data_to_update = data.get('data_to_update')

        # Update company
        Company.update_company(mongo_db, company_id, data_to_update)

        return jsonify({"message": "Company was updated"}), 200

    @companies.route('/hide', methods=["PUT"])
    def hide_company():
        data = request.get_json()
        company_id = data.get('company_id')

        # Update company
        Company.update_company(mongo_db, company_id, {'hidden': True})

        return jsonify({"message": "Company was hid"}), 200

    @companies.route('/restore', methods=["PUT"])
    def restore_company():
        data = request.get_json()
        company_id = data.get('company_id')

        # Update company
        Company.update_company(mongo_db, company_id, {'hidden': False})

        return jsonify({"message": "Company was restored"}), 200

    return companies
