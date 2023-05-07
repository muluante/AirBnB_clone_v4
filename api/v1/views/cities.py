#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_per_state(state_id=None):
    """Cities endpoint handling methods for cities by state"""
    state_obj = storage.get('State', state_id)
    if not state_obj:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_cities = storage.all('City')
        City_List = []
        for obj in all_cities.values():
            if obj.state_id == state_id:
                City_List.append(obj.to_dict())
        return jsonify(City_List)

    if request.method == 'POST':
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        elif 'name' not in req_json:
            abort(400, 'Missing name')
        else:
            new_city = City(**req_json)
            new_city.state_id = state_id
            storage.new(new_city)
            new_city.save()
            storage.close()
            json_data = jsonify(new_city.to_dict())
            return make_response(json_data, 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def cities_with_id(city_id=None):
    """Endpoint to handle methods based on a city id"""
    city_obj = storage.get('City', city_id)
    if not city_obj:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(city_obj.to_dict())

    if request.method == 'DELETE':
        city_obj.delete()
        storage.save()
        storage.close()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        ignore_keys = ['id', 'created_at', 'updated_at', 'state_id']
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        for key, val in req_json.items():
            if key not in ignore_keys:
                setattr(city_obj, key, val)
        city_obj.save()
        storage.close()
        return make_response(jsonify(city_obj.to_dict()), 200)
