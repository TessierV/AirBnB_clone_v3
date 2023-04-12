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
    elif 'name' not in create_amenity:
        abort(400, description="Missing name" )
    else:
        new_amenity = Amenity(**data_json)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """Testing documentation of a module"""
    amenity = storage.get(Amenity, amenity_id)
    request_json = request.get_json()
    if amenity is None:
        abort(404)
    elif request_json is None:
        abort(400, description="Not a JSON")
    else:
        for key, val in request_json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, val)
        storage.save()
        return jsonify(amenity.to_dict()), 200
