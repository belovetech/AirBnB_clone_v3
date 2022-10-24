#!/usr/bin/python3
"""
return status of the page
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """Retrive response status"""
    return jsonify({
        'status': 'OK'
    })


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """retrieves the number of each objects by type"""

    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    })
