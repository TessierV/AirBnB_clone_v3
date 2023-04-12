#!/usr/bin/python3
"""Testing documentation of a module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_place_city():
    """Testing documentation of a module"""
    places_list = []
    if storage.get(City, city_id) is None:
        abort(404)
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_place(place_id):
    """Testing documentation of a module"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif request.method == 'GET':
        place_id = place.to_dict()
        return jsonify(place_id)
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def post_place(city_id):
    """Testing documentation of a module"""
    create_data = request.get_json()
    if storage.get(City, city_id) is None:
        abort(404)

    if create_data is None:
        abort(400, description="Not a JSON")
    elif 'user_id' not in create_data:
        abort(400, description="Missing user_id" )
    elif 'name' not in create_data:
        abort(400, description="Missing name" )
    if storage.get(User, create_data['user_id']) is None:
        abort(404)
    else:
        new_place = Place(**create_data)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Testing documentation of a module"""
    upd_place = storage.get(Place, place_id)
    request_json = request.get_json()
    if upd_place is None:
        abort(404)
    elif request_json is None:
        abort(400, description="Not a JSON")
    else:
        for key, val in request_json.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(upd_place, key, val)
        storage.save()
        return jsonify(upd_place.to_dict()), 200
