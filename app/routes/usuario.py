# app/routes/usuario.py
from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.extensions import db
from app.services.auth_service import generate_token
from app.decorators.PyJWT import token_required

usuario_bp = Blueprint('usuario', __name__)

# Obtener todos los usuarios (solo para administradores)
@usuario_bp.route('/usuarios', methods=['GET'])
@token_required
def get_usuarios(current_user):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    usuarios = Usuario.query.all()
    output = [user.to_dict() for user in usuarios]

    return jsonify({'usuarios': output}), 200

# Obtener un usuario por ID
@usuario_bp.route('/usuarios/<int:id_user>', methods=['GET'])
@token_required
def get_usuario(current_user, id_user):
    if current_user.flag_administrador != '1' and current_user.id_user != id_user:
        return jsonify({"message": "Acceso denegado"}), 403

    user = Usuario.query.get(id_user)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200

# Actualizar un usuario
@usuario_bp.route('/usuarios/<int:id_user>', methods=['PUT'])
@token_required
def update_usuario(current_user, id_user):
    if current_user.flag_administrador != '1' and current_user.id_user != id_user:
        return jsonify({"message": "Acceso denegado"}), 403

    user = Usuario.query.get(id_user)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    data = request.get_json()
    user.login_user = data.get('login_user', user.login_user)
    user.nro_doc_ident = data.get('nro_doc_ident', user.nro_doc_ident)
    user.nombre_user = data.get('nombre_user', user.nombre_user)
    user.direccion_user = data.get('direccion_user', user.direccion_user)
    user.telefono_user = data.get('telefono_user', user.telefono_user)
    if 'password' in data:
        user.set_password(data['password'])
    if current_user.flag_administrador == '1':
        user.flag_administrador = data.get('flag_administrador', user.flag_administrador)
        user.flag_inventarios = data.get('flag_inventarios', user.flag_inventarios)
        user.flag_estado = data.get('flag_estado', user.flag_estado)

    db.session.commit()
    return jsonify({"message": "Usuario actualizado exitosamente"}), 200

# Inactivar un usuario
@usuario_bp.route('/usuarios/<int:id_user>', methods=['DELETE'])
@token_required
def delete_usuario(current_user, id_user):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    user = Usuario.query.get(id_user)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    user.flag_estado = '0'  # Inactivar el usuario
    db.session.commit()
    return jsonify({"message": "Usuario inactivado exitosamente"}), 200