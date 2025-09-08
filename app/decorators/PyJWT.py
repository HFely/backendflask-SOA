# app/decorators/PyJWT.py
import jwt
from functools import wraps
from flask import request, jsonify, current_app
from app.extensions import blacklist
from app.models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token faltante'}), 401

        if token in blacklist:
            return jsonify({'message': 'Token revocado'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except Exception as e:
            return jsonify({'message': 'Token inválido', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)
    return decorated
