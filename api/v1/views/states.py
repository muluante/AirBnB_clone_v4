#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states_no_id():
    """Endpoint to handle methods with no state id included"""
    if request.method == 'GET':
        all_states = storage.all('State')
        objs = [obj.to_dict() for obj in all_states.values()]
        return jsonify(objs)

    if request.method == 'POST':
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        elif 'name' not in req_json:
            abort(400, 'Missing name')
        else:
            new_object = State(**req_json)
            new_object.save()
            json_data = jsonify(new_object.to_dict())
            return make_response(json_data, 201)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def states_with_id(state_id=None):
    """Endpoint to handle http methods with state id"""
    state_obj = storage.get('State', state_id)
    if not state_obj:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        state_obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        ignore_keys = ['id', 'created_at', 'updated_at']
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        for key, val in req_json.items():
            if key not in ignore_keys:
                setattr(state_obj, key, val)
        state_obj.save()
        storage.close()
        return make_response(jsonify(state_obj.to_dict()), 200)
