#!/usr/bin/python3
"""View to handle all amenites objects"""

from models import storage
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Return all amenities objects"""
    amenities = storage.all(Amenity)
    ameni_obj = [a.to_dict() for a in amenities.values()]
    return jsonify(ameni_obj)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get a single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity obj with its id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Post new amenity object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return make_response(new_amenity.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update the amenity object with the provided id"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    ignore_keys = ['id', 'created_id', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(amenity.to_dict(), 200)
