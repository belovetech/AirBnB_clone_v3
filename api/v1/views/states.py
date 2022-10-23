#!/usr/bin/python3
"""
view for the states
"""

import json
from flask import abort, request
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """Retrieves all state objects"""
    all_states = storage.all(State)
    all_states = [obj.to_dict() for obj in all_states.values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves state objects by id"""
    try:
        state = storage.get(State, state_id)
        state = state.to_dict()
    except Exception:
        abort(404)

    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete state by id"""
    try:
        state = storage.get(State, state_id)
        storage.delete(state)
        state.save()
    except Exception:
        abort(404)

    return jsonify({})


@app_views.route('/states', methods=['POST'])
def create_state():
    """Create a state object"""
    data = request.get_json()
    if data is None or not request.is_json:
        abort(404, 'Not a JSON')
    if 'name' not in data:
        abort(404, 'Missing name')

    state = State(**data)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """update state by id"""
    state = storage.get(State, state_id)
    data = request.get_json()
    if not state:
        abort(404)
    if data is None or not request.is_json:
        abort(404, 'Not a JSON')

    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue
        else:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
