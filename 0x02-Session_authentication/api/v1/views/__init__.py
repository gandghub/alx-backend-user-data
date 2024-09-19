#!/usr/bin/env python3
"""
API view initialization file
"""

from flask import Blueprint

# Initialize Blueprint for app views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views after initializing Blueprint to avoid circular imports
from api.v1.views.users import *  # Adjust imports to avoid circular imports
from api.v1.views.session_auth import *  # Adjust this if necessary
