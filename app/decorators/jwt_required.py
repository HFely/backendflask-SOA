# app/decorators/jwt_required.py
from functools import wraps
from flask import request, jsonify
from app.services.auth_service import decode_token
from app.models.user import User
from app.extensions import blacklist

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token faltante"}), 401

        token = auth_header.split(" ")[1]

        if token in blacklist:
            return jsonify({"message": "Token revocado"}), 401

        data = decode_token(token)

        if "error" in data:
            return jsonify({"message": data["error"]}), 401

        current_user = User.query.get(data["user_id"])
        if not current_user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        return f(current_user, *args, **kwargs)
    return decorated
