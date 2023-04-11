#!/usr/bin/python3
""" API Flask app module """
from flask import make_response, Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ closes the storage on teardown """
    if exception:
        storage.close()


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str("Not found")), 404


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', default=5000),
            threaded=True)
