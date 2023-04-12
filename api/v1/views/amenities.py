#!/usr/bin/python3
"""Testing documentation of a module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenity():
    """Testing documentation of a module"""
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_amenity_id(amenity_id):
    """Testing documentation of a module"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif request.method == 'GET':
        amenity_id = amenity.to_dict()
        return jsonify(amenity_id)
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Testing documentation of a module"""
    create_amenity = request.get_json()
    if create_amenity is None:
        abort(400, description="Not a JSON")
    elif 'email' not in create_amenity:
        abort(400, description="Missing email" )
    elif 'password' not in create_amenity:
        abort(400, description="Missing password" )
    else:
        new_user = Amenities(**data_json)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Testing documentation of a module"""
    user = storage.get(Amenities, user_id)
    request_json = request.get_json()
    if user is None:
        abort(404)
    elif request_json is None:
        abort(400, description="Not a JSON")
    else:
        for key, val in request_json.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, val)
        storage.save()
        return jsonify(user.to_dict()), 200
