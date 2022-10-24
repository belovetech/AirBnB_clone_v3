#!/usr/bin/python3
"""
view for the states
"""

import json
from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models.base_model import BaseModel
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves all state objects"""
    all_states = storage.all(State)
    all_states = [obj.to_dict() for obj in all_states.values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves state objects by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    state = state.to_dict()
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    state.delete()
    storage.save()

    return jsonify({}, 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state object"""
    data = request.get_json()
    if data is None or not request.is_json:
        abort(404, 'Not a JSON')
    if 'name' not in data:
        abort(404, 'Missing name')

    state = State(**data)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')

    data = request.get_json()
    if not state:
        abort(404)
    if data is None or not request.is_json:
        abort(404, 'Not a JSON')

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict(), 200)
