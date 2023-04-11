#!/usr/bin/python3
""" API Flask app module """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ closes the storage on teardown """
    if exception:
        storage.close()


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'),
            threaded=True)
