# app/routes/auth_docs.py
from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario  # Cambiado de User a Usuario
from app.extensions import db, blacklist
from app.services.auth_service import generate_token
from app.decorators.PyJWT import token_required
from flask_restx import Resource, fields, Namespace, reqparse

# Crear namespace para Swagger
auth_ns = Namespace('auth', description='Operaciones de autenticación y usuarios')

# Modelos para la documentación Swagger
register_model = auth_ns.model('Registro', {
    'login_user': fields.String(required=True, description='Nombre de usuario para login'),
    'nro_doc_ident': fields.String(required=True, description='Número de documento de identidad'),
    'nombre_user': fields.String(required=True, description='Nombre completo del usuario'),
    'password': fields.String(required=True, description='Contraseña'),
    'direccion_user': fields.String(description='Dirección del usuario'),
    'telefono_user': fields.String(description='Teléfono del usuario'),
    'id_tipo_doc_ident': fields.Integer(default=1, description='ID del tipo de documento')
})

login_model = auth_ns.model('Login', {
    'login_user': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña')
})

update_model = auth_ns.model('ActualizarUsuario', {
    'login_user': fields.String(description='Nuevo nombre de usuario'),
    'nro_doc_ident': fields.String(description='Nuevo número de documento'),
    'nombre_user': fields.String(description='Nuevo nombre completo'),
    'direccion_user': fields.String(description='Nueva dirección'),
    'telefono_user': fields.String(description='Nuevo teléfono'),
    'id_tipo_doc_ident': fields.Integer(description='Nuevo ID tipo documento'),
    'password': fields.String(description='Nueva contraseña')
})

change_password_model = auth_ns.model('CambiarPassword', {
    'old_password': fields.String(required=True, description='Contraseña actual'),
    'new_password': fields.String(required=True, description='Nueva contraseña')
})

reset_password_model = auth_ns.model('ResetPassword', {
    'login_user': fields.String(required=True, description='Nombre de usuario'),
    'nro_doc_ident': fields.String(required=True, description='Número de documento'),
    'id_tipo_doc_ident': fields.Integer(required=True, description='ID tipo documento'),
    'new_password': fields.String(required=True, description='Nueva contraseña')
})

user_response_model = auth_ns.model('UsuarioResponse', {
    'id_user': fields.Integer(description='ID del usuario'),
    'login_user': fields.String(description='Nombre de usuario'),
    'nombre_user': fields.String(description='Nombre completo'),
    'nro_doc_ident': fields.String(description='Número de documento'),
    'direccion_user': fields.String(description='Dirección'),
    'telefono_user': fields.String(description='Teléfono'),
    'flag_administrador': fields.String(description='Flag administrador'),
    'flag_inventarios': fields.String(description='Flag inventarios'),
    'flag_estado': fields.String(description='Estado del usuario')
})

login_response_model = auth_ns.model('LoginResponse', {
    'access_token': fields.String(description='Token JWT'),
    'user': fields.Nested(user_response_model)
})

# Parser para headers de autorización
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

# Endpoints con Swagger Documentation
@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'Usuario registrado exitosamente')
    @auth_ns.response(400, 'Datos inválidos o usuario ya existe')
    def post(self):
        """Registrar un nuevo usuario"""
        data = request.get_json()
        login_user = data.get("login_user")
        nro_doc_ident = data.get("nro_doc_ident")
        nombre_user = data.get("nombre_user")
        password = data.get("password")
        
        # Campos opcionales
        direccion_user = data.get("direccion_user", "")
        telefono_user = data.get("telefono_user", "")
        id_tipo_doc_ident = data.get("id_tipo_doc_ident", 1)

        # Validaciones
        if not all([login_user, nro_doc_ident, nombre_user, password, id_tipo_doc_ident]):
            return {"message": "Faltan campos obligatorios"}, 400

        if Usuario.query.filter_by(login_user=login_user).first():
            return {"message": "El usuario ya existe"}, 400

        if Usuario.query.filter_by(id_tipo_doc_ident=id_tipo_doc_ident, nro_doc_ident=nro_doc_ident).first():
            return {"message": "Ya existe un usuario con este documento"}, 400

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

        return {"message": "Usuario registrado exitosamente"}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login exitoso', login_response_model)
    @auth_ns.response(401, 'Credenciales incorrectas')
    def post(self):
        """Iniciar sesión de usuario"""
        data = request.get_json()
        login_user = data.get("login_user")
        password = data.get("password")

        user = Usuario.query.filter_by(login_user=login_user).first()
        if user and user.check_password(password):
            token = generate_token(user.id_user)
            return {
                "access_token": token,
                "user": {
                    "id_user": user.id_user,
                    "login_user": user.login_user,
                    "nombre_user": user.nombre_user,
                    "flag_administrador": user.flag_administrador,
                    "flag_inventarios": user.flag_inventarios
                }
            }, 200

        return {"message": "Usuario o contraseña incorrectos"}, 401

@auth_ns.route('/logout')
class Logout(Resource):
    @auth_ns.expect(auth_parser)
    @auth_ns.response(200, 'Logout exitoso')
    @auth_ns.response(401, 'Token inválido o faltante')
    def post(self):
        """Cerrar sesión y revocar token"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        blacklist.add(token)
        return {"message": "Logout exitoso, token revocado"}, 200

@auth_ns.route('/delete_account')
class DeleteAccount(Resource):
    @auth_ns.expect(auth_parser)
    @auth_ns.response(200, 'Cuenta eliminada exitosamente')
    @auth_ns.response(401, 'Token inválido o faltante')
    def delete(self):
        """Eliminar cuenta de usuario actual"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        data = decode_token(token)
        if "error" in data:
            return {"message": data["error"]}, 401
            
        current_user = Usuario.query.get(data["user_id"])
        if not current_user:
            return {"message": "Usuario no encontrado"}, 404

        db.session.delete(current_user)
        db.session.commit()
        return {"message": "Cuenta eliminada exitosamente"}, 200

@auth_ns.route('/update_account')
class UpdateAccount(Resource):
    @auth_ns.expect(auth_parser, update_model)
    @auth_ns.response(200, 'Cuenta actualizada exitosamente')
    @auth_ns.response(401, 'Token inválido o faltante')
    def put(self):
        """Actualizar información del usuario actual"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user:
            return {"message": "Usuario no encontrado"}, 404
        
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
        return {"message": "Cuenta actualizada exitosamente"}, 200

@auth_ns.route('/change_password')
class ChangePassword(Resource):
    @auth_ns.expect(auth_parser, change_password_model)
    @auth_ns.response(200, 'Contraseña cambiada exitosamente')
    @auth_ns.response(400, 'Contraseña actual incorrecta')
    @auth_ns.response(401, 'Token inválido o faltante')
    def put(self):
        """Cambiar contraseña del usuario actual"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user:
            return {"message": "Usuario no encontrado"}, 404

        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not current_user.check_password(old_password):
            return {"message": "La contraseña actual es incorrecta"}, 400

        current_user.set_password(new_password)
        db.session.commit()
        return {"message": "Contraseña cambiada exitosamente"}, 200

@auth_ns.route('/reset_password')
class ResetPassword(Resource):
    @auth_ns.expect(reset_password_model)
    @auth_ns.response(200, 'Contraseña restablecida exitosamente')
    @auth_ns.response(404, 'Usuario no encontrado')
    def post(self):
        """Restablecer contraseña (sin autenticación requerida)"""
        data = request.get_json()
        login_user = data.get("login_user")
        nro_doc_ident = data.get("nro_doc_ident")
        id_tipo_doc_ident = data.get("id_tipo_doc_ident")
        new_password = data.get("new_password")

        user = Usuario.query.filter_by(
            login_user=login_user, 
            nro_doc_ident=nro_doc_ident, 
            id_tipo_doc_ident=id_tipo_doc_ident
        ).first()
        
        if not user:
            return {"message": "Usuario no encontrado con los datos proporcionados"}, 404

        user.set_password(new_password)
        db.session.commit()
        return {"message": "Contraseña restablecida exitosamente"}, 200

@auth_ns.route('/me')
class GetCurrentUser(Resource):
    @auth_ns.expect(auth_parser)
    @auth_ns.response(200, 'Datos del usuario', user_response_model)
    @auth_ns.response(401, 'Token inválido o faltante')
    def get(self):
        """Obtener información del usuario actual"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user:
            return {"message": "Usuario no encontrado"}, 404

        return {
            "id_user": current_user.id_user,
            "login_user": current_user.login_user,
            "nombre_user": current_user.nombre_user,
            "nro_doc_ident": current_user.nro_doc_ident,
            "direccion_user": current_user.direccion_user,
            "telefono_user": current_user.telefono_user,
            "flag_administrador": current_user.flag_administrador,
            "flag_inventarios": current_user.flag_inventarios,
            "flag_estado": current_user.flag_estado
        }, 200
