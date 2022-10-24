#!/usr/bin/python3
"""
view for the states
"""

from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves all state objects"""
    all_states = storage.all('State')
    all_states = [obj.to_dict() for obj in all_states.values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves state objects by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    return jsonify(state.to_dict())


# @app_views.route('/states/<state_id>',
#                  methods=['DELETE'], strict_slashes=False)
# def del_state(state_id):
#     """Delete a state obj with its id"""
#     state = storage.get(State, state_id)
#     if not state:
#         abort(404)
#     state.delete()
#     storage.save()
#     return make_response({}, 200)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state by id"""
    try:
        state = storage.get(State, state_id)
    # if state is None:
    #     abort(404, 'Not found')
        state.delete()
        storage.save()
    except Exception:
        abort(404, 'Not found')
    return make_response({}, 200)


# @app_views.route('/states', methods=['POST'], strict_slashes=False)
# def create_state():
#     """Create a new state object"""
#     data = request.get_json()
#     if data is None or not request.is_json:
#         abort(404, 'Not a JSON')
#     if 'name' not in data:
#         abort(404, 'Missing name')

#     state = State(**data)
#     state.save()

#     return make_response(state.to_dict(), 201)


# @app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
# def update_state(state_id):
#     """update state by id"""
#     state = storage.get(State, state_id)
#     if state is None:
#         abort(404, 'Not found')

#     data = request.get_json()
#     if data is None or not data.is_json:
#         abort(404, 'Not a JSON')

#     ignore_keys = ['id', 'created_at', 'updated_at']
#     for key, value in data.items():
#         if key not in ignore_keys:
#             setattr(state, key, value)
#     state.save()
#     return make_response(state.to_dict(), 200)


# @app_views.route('/states', methods=['GET'], strict_slashes=False)
# def all_states():
#     """Return all states objects"""
#     states = storage.all('State')
#     statess = []
#     for state in states.values():
#         statess.append(state.to_dict())
#     return jsonify(statess)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Post new state object"""
    post_req = request.get_json()
    if not post_req:
        abort(400, "Not a JSON")
    if 'name' not in post_req:
        abort(400, "Missing name")

    new_state = State(**post_req)
    storage.new(new_state)
    storage.save()
    return make_response(new_state.to_dict(), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update the state object with the provided id"""
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    ignore_keys = ['id', 'created_id', 'updated_at']

    for key, value in put_req.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return make_response(state.to_dict(), 200)
