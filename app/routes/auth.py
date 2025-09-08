# app/routes/auth.py
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db, blacklist
from app.services.auth_service import generate_token
from app.decorators.PyJWT import token_required

auth_bp = Blueprint('auth', __name__)

#registro de usuario
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "El usuario ya existe"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

#logueo de usuario
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = generate_token(user.id)
        return jsonify({"access_token": token}), 200

    return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

#deslogueo de usuario
@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    token = request.headers['Authorization'].split(" ")[1]
    blacklist.add(token)
    return jsonify({"message": "Logout exitoso, token revocado"}), 200

#eliminacion de usuario
@auth_bp.route('/delete_account', methods=['DELETE'])
@token_required
def delete_account(current_user):
    db.session.delete(current_user)
    db.session.commit()
    return jsonify({"message": "Cuenta eliminada exitosamente"}), 200

#acctualizacion de usuario
@auth_bp.route('/update_account', methods=['PUT'])
@token_required
def update_account(current_user):
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if username:
        current_user.username = username
    if email:
        current_user.email = email
    if password:
        current_user.set_password(password)

    db.session.commit()
    return jsonify({"message": "Cuenta actualizada exitosamente"}), 200