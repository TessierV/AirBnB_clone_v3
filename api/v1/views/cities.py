#!/usr/bin/python3
"""Testing documentation of a module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """Testing documentation of a module"""
    cities_list = []
    if storage.get(State, state_id) is None:
        abort(404)
    for city in storage.all(City).values():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_city(city_id):
    """Testing documentation of a module"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    elif request.method == 'GET':
        city_id = city.to_dict()
        return jsonify(city_id)
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Testing documentation of a module"""
    create_data = request.get_json()

    if create_data is None:
        abort(400, description="Not a JSON")
    elif 'name' not in create_data:
        abort(400, description="Missing name" )
    elif storage.get(State, state_id) is None:
        abort(404)
    else:
        new_city = City(**create_data)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(user_id):
    """Testing documentation of a module"""
    city = storage.get(City, city_id)
    request_json = request.get_json()
    if city is None:
        abort(404)
    elif request_json is None:
        abort(400, description="Not a JSON")
    else:
        for key, val in request_json.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        storage.save()
        return jsonify(city.to_dict()), 200
