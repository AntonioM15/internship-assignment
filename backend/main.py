from flask import Flask, jsonify

from routes.landing import landing_blueprint

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# Register all blueprints (files where endpoints are located)
app.register_blueprint(landing_blueprint, url_prefix="/api/v1/landing")


if __name__ == '__main__':
    app.run(debug=True)
