#!/usr/bin/python3
""" Index file """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/stats', strict_slashes=False)
def app_views_stats():
    """ Create an endpoint that retrieves
    the number of each objects by type """
    stats_obj = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats_obj)


@app_views.route("/status", strict_slashes=False)
def status():
    return jsonify({"status": "OK"})
