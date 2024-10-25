from flask import current_app, request, jsonify
from functools import wraps
import jwt
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()  # Ensure the token is valid before proceeding
        return f(*args, **kwargs)
    return decorated

# Custom admin_required decorator for role-based access control
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        identity = get_jwt_identity()  # Ensure the token has already been validated
        if identity['role'] != 'Admin':  # Assuming 'role' is stored in the token
            return jsonify({'message': 'Admins only!'}), 403  
        return f(*args, **kwargs)

    return decorated

