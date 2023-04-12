#!/usr/bin/python3
"""
Modules User
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    users_list = []
    for user in storage.all(User).values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_user_id(user_id):
    """
    retrieves a User by its id and delete
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    elif request.method == 'GET':
        user_id = user.to_dict()
        return jsonify(user_id)
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """
    creates a User
    """
    create_user = request.get_json()
    if create_user is None:
        abort(400, description="Not a JSON")
    elif 'email' not in create_user:
        abort(400, description="Missing email" )
    elif 'password' not in create_user:
        abort(400, description="Missing password" )
    else:
        new_user = User(**data_json)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """
    updates a User
    """
    user = storage.get(User, user_id)
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
