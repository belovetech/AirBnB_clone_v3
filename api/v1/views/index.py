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
