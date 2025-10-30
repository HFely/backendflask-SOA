# app/routes/auth.py
from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario  # Cambiado de User a Usuario
from app.extensions import db, blacklist
from app.services.auth_service import generate_token
from app.decorators.PyJWT import token_required

auth_bp = Blueprint('auth', __name__)

# Mantener endpoints tradicionales para compatibilidad (opcional)
#registro de usuario
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    login_user = data.get("login_user")  # Cambiado de username a login_user
    nro_doc_ident = data.get("nro_doc_ident")
    nombre_user = data.get("nombre_user")
    password = data.get("password")
    
    # Campos opcionales
    direccion_user = data.get("direccion_user", "")
    telefono_user = data.get("telefono_user", "")
    id_tipo_doc_ident = data.get("id_tipo_doc_ident", 1)  # Valor por defecto

    # Validaciones
    if not all([login_user, nro_doc_ident, nombre_user, password, id_tipo_doc_ident]):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    if Usuario.query.filter_by(login_user=login_user).first():
        return jsonify({"message": "El usuario ya existe"}), 400

    # Verificar que no exista otro usuario con el mismo nro_doc_ident y tipo
    if Usuario.query.filter_by(id_tipo_doc_ident=id_tipo_doc_ident, nro_doc_ident=nro_doc_ident).first():
        return jsonify({"message": "Ya existe un usuario con este documento"}), 400

    user = Usuario(
        login_user=login_user,
        id_tipo_doc_ident=id_tipo_doc_ident,
        nro_doc_ident=nro_doc_ident,
        nombre_user=nombre_user,
        direccion_user=direccion_user,
        telefono_user=telefono_user
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

#logueo de usuario
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login_user = data.get("login_user")  # Cambiado de username a login_user
    password = data.get("password")

    user = Usuario.query.filter_by(login_user=login_user).first()
    if user and user.check_password(password):
        token = generate_token(user.id_user)  # Cambiado de user.id a user.id_user
        return jsonify({
            "access_token": token,
            "user": {
                "id_user": user.id_user,
                "login_user": user.login_user,
                "nombre_user": user.nombre_user,
                "flag_administrador": user.flag_administrador,
                "flag_inventarios": user.flag_inventarios
            }
        }), 200

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

#actualizacion de usuario
@auth_bp.route('/update_account', methods=['PUT'])
@token_required
def update_account(current_user):
    data = request.get_json()
    
    if 'login_user' in data:
        current_user.login_user = data.get("login_user")
    if 'nro_doc_ident' in data:
        current_user.nro_doc_ident = data.get("nro_doc_ident")
    if 'nombre_user' in data:
        current_user.nombre_user = data.get("nombre_user")
    if 'direccion_user' in data:
        current_user.direccion_user = data.get("direccion_user")
    if 'telefono_user' in data:
        current_user.telefono_user = data.get("telefono_user")
    if 'id_tipo_doc_ident' in data:
        current_user.id_tipo_doc_ident = data.get("id_tipo_doc_ident")
    if 'password' in data:
        current_user.set_password(data.get("password"))

    db.session.commit()
    return jsonify({"message": "Cuenta actualizada exitosamente"}), 200

#cambio de contraseña
@auth_bp.route('/change_password', methods=['PUT'])
@token_required
def change_password(current_user):
    data = request.get_json()
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not current_user.check_password(old_password):
        return jsonify({"message": "La contraseña actual es incorrecta"}), 400

    current_user.set_password(new_password)
    db.session.commit()
    return jsonify({"message": "Contraseña cambiada exitosamente"}), 200

#recuperacion de contraseña
@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    login_user = data.get("login_user")  # Cambiado de username a login_user
    nro_doc_ident = data.get("nro_doc_ident")
    id_tipo_doc_ident = data.get("id_tipo_doc_ident")
    new_password = data.get("new_password")

    user = Usuario.query.filter_by(login_user=login_user, nro_doc_ident=nro_doc_ident, id_tipo_doc_ident=id_tipo_doc_ident).first()
    if not user:
        return jsonify({"message": "Usuario no encontrado con los datos proporcionados"}), 404

    user.set_password(new_password)
    db.session.commit()
    return jsonify({"message": "Contraseña restablecida exitosamente"}), 200

# Obtener información del usuario actual
@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({
        "id_user": current_user.id_user,
        "login_user": current_user.login_user,
        "nombre_user": current_user.nombre_user,
        "nro_doc_ident": current_user.nro_doc_ident,
        "direccion_user": current_user.direccion_user,
        "telefono_user": current_user.telefono_user,
        "flag_administrador": current_user.flag_administrador,
        "flag_inventarios": current_user.flag_inventarios,
        "flag_estado": current_user.flag_estado
    }), 200