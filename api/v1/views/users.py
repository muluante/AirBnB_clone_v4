#!/usr/bin/python3
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'], strict_slashes=False)
def users_no_id():
    """Endpoint that handles http requests with no ID given"""

    if request.method == 'GET':
        all_users = storage.all('User')
        User_List = []
        for obj in all_users.values():
            User_List.append(obj.to_dict())
        return jsonify(User_List)

    if request.method == 'POST':
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        elif 'email' not in req_json:
            abort(400, 'Missing email')
        elif 'password' not in req_json:
            abort(400, 'Missing password')
        else:
            new_User = User(**req_json)
            storage.new(new_User)
            new_User.save()
            storage.close()
            return jsonify(new_User.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_with_id(user_id=None):
    """Endpoint that handles http requests with ID given"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(user_obj.to_dict())

    if request.method == 'DELETE':
        user_obj.delete()
        storage.save()
        storage.close()
        return jsonify({}), 200

    if request.method == 'PUT':
        ignore_keys = ['id', 'created_at', 'updated_at', 'email']
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        for key, val in req_json.items():
            if key not in ignore_keys:
                setattr(user_obj, key, val)
        user_obj.save()
        storage.close()
        return jsonify(user_obj.to_dict()), 200
