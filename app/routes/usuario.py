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
def ConsultarUsuarios(current_user):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    usuarios = Usuario.query.all()
    output = [user.to_dict() for user in usuarios]

    return jsonify({'usuarios': output}), 200

# Obtener un usuario por ID
@usuario_bp.route('/usuarios/<int:id_user>', methods=['GET'])
@token_required
def ConsultarUsuarioID(current_user, id_user):
    if current_user.flag_administrador != '1' and current_user.id_user != id_user:
        return jsonify({"message": "Acceso denegado"}), 403

    user = Usuario.query.get(id_user)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(user.to_dict()), 200

# Crear un nuevo usuario (solo para administradores)
@usuario_bp.route('/usuarios', methods=['POST'])
@token_required
def CrearUsuario(current_user):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    data = request.get_json()
    login_user = data.get("login_user")
    nro_doc_ident = data.get("nro_doc_ident")
    nombre_user = data.get("nombre_user")
    password = data.get("password")
    
    # Campos opcionales
    direccion_user = data.get("direccion_user", "")
    telefono_user = data.get("telefono_user", "")
    id_tipo_doc_ident = data.get("id_tipo_doc_ident", 1)  # Valor por defecto
    flag_administrador = data.get("flag_administrador", '0')
    flag_inventarios = data.get("flag_inventarios", '0')
    flag_estado = data.get("flag_estado", '1')

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
        telefono_user=telefono_user,
        flag_administrador=flag_administrador,
        flag_inventarios=flag_inventarios,
        flag_estado=flag_estado
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente"}), 201

# Actualizar un usuario
@usuario_bp.route('/usuarios/<int:id_user>', methods=['PUT'])
@token_required
def ModificarUsuario(current_user, id_user):
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
def InactivarUsuario(current_user, id_user):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    user = Usuario.query.get(id_user)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    user.flag_estado = '0'  # Inactivar el usuario
    db.session.commit()
    return jsonify({"message": "Usuario inactivado exitosamente"}), 200

