from flask import Flask, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_session import Session
from google.cloud import secretmanager
import os

from routes.test_routes import test_routes_blueprint
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
if os.getenv('LOCAL_DEV') or os.getenv("TEST_ENV"):
    MONGO_URI = "mongodb://localhost:27017/tfm_local_db"
    SESSION_KEY = "this_secret_key_is_not_real"
    STATIC_FOLDER = "../frontend/dist/static"
    TEMPLATE_FOLDER = "../frontend/dist"
else:
    MONGO_URI = get_secret('MONGO_URI')
    SESSION_KEY = get_secret('SESSION_KEY')
    STATIC_FOLDER = "dist/static"
    TEMPLATE_FOLDER = "dist"

app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            template_folder=TEMPLATE_FOLDER)
CORS(app, supports_credentials=True, origins=["http://localhost:5000"])

# Session base config
app.secret_key = SESSION_KEY
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Init Mongo first
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# Use MongoDB for sessions
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = mongo.cx
app.config['SESSION_MONGODB_DB'] = mongo.db.name
app.config['SESSION_MONGODB_COLLECT'] = 'flask_sessions'

# Cookie flags
app.config['SESSION_COOKIE_SECURE'] = not IS_LOCAL  # only https connections
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # for cross-site requests

# Init Flask-Session
Session(app)

# Register all blueprints with deferred initialization in order to share the same mongodb
app.register_blueprint(landing_blueprint(mongo), url_prefix="/api/v1/landing")
app.register_blueprint(dashboard_blueprint(mongo), url_prefix="/api/v1/dashboard")
app.register_blueprint(students_blueprint(mongo), url_prefix="/api/v1/students")
app.register_blueprint(tutors_blueprint(mongo), url_prefix="/api/v1/tutors")
app.register_blueprint(companies_blueprint(mongo), url_prefix="/api/v1/companies")
app.register_blueprint(assignments_blueprint(mongo), url_prefix="/api/v1/assignments")
app.register_blueprint(test_routes_blueprint(mongo), url_prefix="/api/v1/test_routes")
# TODO remove
app.register_blueprint(testing_users_blueprint(mongo), url_prefix="/api/v1/testing_users")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def render_vue(path):
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
