from flask import Flask, render_template
from flask_pymongo import PyMongo
from google.cloud import secretmanager
import os

from routes.assignments import assignments_blueprint
from routes.companies import companies_blueprint
from routes.dashboard import dashboard_blueprint
from routes.students import students_blueprint
from routes.landing import landing_blueprint
from routes.testing_users import testing_users_blueprint
from routes.tutors import tutors_blueprint


def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/1"
    response = client.access_secret_version(request={"name": secret_path})
    return response.payload.data.decode('UTF-8')


# Load env variables to decide which env to use
if os.getenv('LOCAL_DEV'):
    MONGO_URI = "mongodb://localhost:27017/tfm_local_db"
    STATIC_FOLDER = "../frontend/dist/static"
    TEMPLATE_FOLDER = "../frontend/dist"
else:
    MONGO_URI = get_secret('MONGO_URI')
    STATIC_FOLDER = "dist/static"
    TEMPLATE_FOLDER = "dist"

app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            template_folder=TEMPLATE_FOLDER)
# Init mongo config
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# Register all blueprints with deferred initialization in order to share the same mongodb
# TODO add a blueprint with url / that redirects to landing or dashboard
app.register_blueprint(assignments_blueprint(mongo), url_prefix="/api/v1/assignments")
app.register_blueprint(companies_blueprint(mongo), url_prefix="/api/v1/companies")
app.register_blueprint(dashboard_blueprint(mongo), url_prefix="/api/v1/dashboard")
app.register_blueprint(students_blueprint(mongo), url_prefix="/api/v1/students")
app.register_blueprint(landing_blueprint(mongo), url_prefix="/api/v1/landing")
app.register_blueprint(testing_users_blueprint(mongo), url_prefix="/api/v1/testing_users")
app.register_blueprint(tutors_blueprint(mongo), url_prefix="/api/v1/tutors")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def render_vue(path):
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
