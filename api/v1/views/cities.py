#!/usr/bin/python3
"""
view for the cities
"""
from flask import abort, request, make_response, jsonify
from models.base_model import BaseModel
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def get_all_cities(state_id):
    """Retrieves all cities in a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    # all_cities = storage.all(City)
    # cities = [city.to_dict() for city in all_cities.values()
    # if city.state_id == state_id]
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new city object"""
    data = request.get_json()
    if not data:
        abort(404, 'Not a JSON')
    if 'name' not in data:
        abort(404, 'Missing name')
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    new_city = City(**data)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return make_response(new_city.to_dict(), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city object"""
    data = request.get_json()
    if not data:
        abort(404, 'Not a JSON')
    city = storage.get(City, city_id)
    if not city:
        abort(404, 'Not found')

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return make_response(city.to_dict(), 200)
