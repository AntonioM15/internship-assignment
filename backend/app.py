from flask import Flask, render_template
from flask_pymongo import PyMongo

from routes.dashboard import dashboard_blueprint
from routes.landing import landing_blueprint
from routes.testing_users import testing_users_blueprint


app = Flask(__name__,
            static_folder="../frontend/dist/static",
            template_folder="../frontend/dist")
# Init mongo config
app.config["MONGO_URI"] = "mongodb://localhost:27017/tfm_local_db"
mongo = PyMongo(app)

# Register all blueprints with deferred initialization in order to share the same mongodb
# TODO add a blueprint with url / that redirects to landing or dashboard
app.register_blueprint(dashboard_blueprint(mongo), url_prefix="/api/v1/dashboard")
app.register_blueprint(landing_blueprint(mongo), url_prefix="/api/v1/landing")
app.register_blueprint(testing_users_blueprint(mongo), url_prefix="/api/v1/testing_users")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def render_vue(path):
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
