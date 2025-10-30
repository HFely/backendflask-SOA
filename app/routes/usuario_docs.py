from flask import request
from flask_restx import Resource, fields, Namespace, reqparse
from app.models.usuario import Usuario
from app.extensions import db

# Crear namespace para Swagger
usuario_ns = Namespace('usuarios', description='Operaciones de gestión de usuarios')

# Modelos para la documentación Swagger
usuario_model = usuario_ns.model('Usuario', {
    'id_user': fields.Integer(readOnly=True, description='ID único del usuario'),
    'login_user': fields.String(required=True, description='Nombre de usuario para login'),
    'nro_doc_ident': fields.String(required=True, description='Número de documento de identidad'),
    'nombre_user': fields.String(required=True, description='Nombre completo del usuario'),
    'direccion_user': fields.String(description='Dirección del usuario'),
    'telefono_user': fields.String(description='Teléfono del usuario'),
    'id_tipo_doc_ident': fields.Integer(required=True, description='ID del tipo de documento'),
    'flag_administrador': fields.String(description='Indica si es administrador (1:Sí, 0:No)'),
    'flag_inventarios': fields.String(description='Indica si tiene permisos de inventario (1:Sí, 0:No)'),
    'flag_estado': fields.String(description='Estado del usuario (1:Activo, 0:Inactivo)')
})

usuario_create_model = usuario_ns.model('CrearUsuario', {
    'login_user': fields.String(required=True, description='Nombre de usuario para login'),
    'nro_doc_ident': fields.String(required=True, description='Número de documento de identidad'),
    'nombre_user': fields.String(required=True, description='Nombre completo del usuario'),
    'password': fields.String(required=True, description='Contraseña del usuario'),
    'direccion_user': fields.String(description='Dirección del usuario'),
    'telefono_user': fields.String(description='Teléfono del usuario'),
    'id_tipo_doc_ident': fields.Integer(default=1, description='ID del tipo de documento'),
    'flag_administrador': fields.String(default='0', description='Indica si es administrador'),
    'flag_inventarios': fields.String(default='0', description='Indica si tiene permisos de inventario'),
    'flag_estado': fields.String(default='1', description='Estado del usuario')
})

usuario_update_model = usuario_ns.model('ActualizarUsuario', {
    'login_user': fields.String(description='Nombre de usuario para login'),
    'nro_doc_ident': fields.String(description='Número de documento de identidad'),
    'nombre_user': fields.String(description='Nombre completo del usuario'),
    'password': fields.String(description='Nueva contraseña'),
    'direccion_user': fields.String(description='Dirección del usuario'),
    'telefono_user': fields.String(description='Teléfono del usuario'),
    'flag_administrador': fields.String(description='Indica si es administrador'),
    'flag_inventarios': fields.String(description='Indica si tiene permisos de inventario'),
    'flag_estado': fields.String(description='Estado del usuario')
})

usuario_response_model = usuario_ns.model('UsuarioResponse', {
    'id_user': fields.Integer(description='ID único del usuario'),
    'login_user': fields.String(description='Nombre de usuario'),
    'nro_doc_ident': fields.String(description='Número de documento'),
    'nombre_user': fields.String(description='Nombre completo'),
    'direccion_user': fields.String(description='Dirección'),
    'telefono_user': fields.String(description='Teléfono'),
    'id_tipo_doc_ident': fields.Integer(description='ID del tipo de documento'),
    'flag_administrador': fields.String(description='Es administrador'),
    'flag_inventarios': fields.String(description='Permisos de inventario'),
    'flag_estado': fields.String(description='Estado del usuario')
})

# Parser para headers de autorización
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

# Endpoints con Swagger Documentation
@usuario_ns.route('/')
class UsuarioList(Resource):
    @usuario_ns.expect(auth_parser)
    @usuario_ns.response(200, 'Lista de usuarios obtenida exitosamente')
    @usuario_ns.response(401, 'Token inválido o faltante')
    @usuario_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @usuario_ns.marshal_list_with(usuario_response_model)
    def get(self):
        """Obtener todos los usuarios (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        usuarios = Usuario.query.filter_by(flag_estado='1').all()
        return [usuario.to_dict() for usuario in usuarios], 200

    @usuario_ns.expect(auth_parser, usuario_create_model)
    @usuario_ns.response(201, 'Usuario creado exitosamente')
    @usuario_ns.response(400, 'Datos inválidos o usuario ya existe')
    @usuario_ns.response(401, 'Token inválido o faltante')
    @usuario_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    def post(self):
        """Crear un nuevo usuario (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        login_user = data.get("login_user")
        nro_doc_ident = data.get("nro_doc_ident")
        nombre_user = data.get("nombre_user")
        password = data.get("password")
        direccion_user = data.get("direccion_user", "")
        telefono_user = data.get("telefono_user", "")
        id_tipo_doc_ident = data.get("id_tipo_doc_ident", 1)
        flag_administrador = data.get("flag_administrador", '0')
        flag_inventarios = data.get("flag_inventarios", '0')
        flag_estado = data.get("flag_estado", '1')

        # Validaciones
        required_fields = ['login_user', 'nro_doc_ident', 'nombre_user', 'password']
        if not all(data.get(field) for field in required_fields):
            return {"message": "Faltan campos obligatorios: login_user, nro_doc_ident, nombre_user, password"}, 400

        # Validar unicidad del login
        if Usuario.query.filter_by(login_user=login_user).first():
            return {"message": "El nombre de usuario ya existe"}, 400

        # Validar unicidad del documento
        if Usuario.query.filter_by(id_tipo_doc_ident=id_tipo_doc_ident, nro_doc_ident=nro_doc_ident).first():
            return {"message": "Ya existe un usuario con este documento de identidad"}, 400

        usuario = Usuario(
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
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()

        return {
            "message": "Usuario creado exitosamente", 
            "id_user": usuario.id_user
        }, 201

@usuario_ns.route('/<int:id_user>')
class UsuarioDetail(Resource):
    @usuario_ns.expect(auth_parser)
    @usuario_ns.response(200, 'Usuario obtenido exitosamente', usuario_response_model)
    @usuario_ns.response(401, 'Token inválido o faltante')
    @usuario_ns.response(403, 'Acceso denegado')
    @usuario_ns.response(404, 'Usuario no encontrado')
    def get(self, id_user):
        """Obtener un usuario por ID"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user:
            return {"message": "Usuario no encontrado"}, 404

        # Solo administradores o el propio usuario pueden ver los datos
        if current_user.flag_administrador != '1' and current_user.id_user != id_user:
            return {"message": "Acceso denegado"}, 403

        usuario = Usuario.query.get(id_user)
        if not usuario or usuario.flag_estado != '1':
            return {"message": "Usuario no encontrado"}, 404

        return usuario.to_dict(), 200

    @usuario_ns.expect(auth_parser, usuario_update_model)
    @usuario_ns.response(200, 'Usuario actualizado exitosamente')
    @usuario_ns.response(400, 'Datos inválidos o conflictos')
    @usuario_ns.response(401, 'Token inválido o faltante')
    @usuario_ns.response(403, 'Acceso denegado')
    @usuario_ns.response(404, 'Usuario no encontrado')
    def put(self, id_user):
        """Actualizar un usuario"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user:
            return {"message": "Usuario no encontrado"}, 404

        # Solo administradores o el propio usuario pueden actualizar
        if current_user.flag_administrador != '1' and current_user.id_user != id_user:
            return {"message": "Acceso denegado"}, 403

        usuario = Usuario.query.get(id_user)
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404

        # Validar unicidad del login si se está cambiando
        if 'login_user' in data and data['login_user'] != usuario.login_user:
            if Usuario.query.filter_by(login_user=data['login_user']).first():
                return {"message": "El nombre de usuario ya existe"}, 400

        # Validar unicidad del documento si se está cambiando
        if ('nro_doc_ident' in data and data['nro_doc_ident'] != usuario.nro_doc_ident) or \
           ('id_tipo_doc_ident' in data and data['id_tipo_doc_ident'] != usuario.id_tipo_doc_ident):
            
            nro_doc = data.get('nro_doc_ident', usuario.nro_doc_ident)
            tipo_doc = data.get('id_tipo_doc_ident', usuario.id_tipo_doc_ident)
            
            existing = Usuario.query.filter(
                Usuario.nro_doc_ident == nro_doc,
                Usuario.id_tipo_doc_ident == tipo_doc,
                Usuario.id_user != id_user
            ).first()
            
            if existing:
                return {"message": "Ya existe otro usuario con este documento de identidad"}, 400

        # Actualizar campos básicos (todos los usuarios pueden actualizar sus datos básicos)
        if 'login_user' in data:
            usuario.login_user = data['login_user']
        if 'nro_doc_ident' in data:
            usuario.nro_doc_ident = data['nro_doc_ident']
        if 'nombre_user' in data:
            usuario.nombre_user = data['nombre_user']
        if 'direccion_user' in data:
            usuario.direccion_user = data['direccion_user']
        if 'telefono_user' in data:
            usuario.telefono_user = data['telefono_user']
        if 'password' in data:
            usuario.set_password(data['password'])

        # Solo administradores pueden actualizar flags y estado
        if current_user.flag_administrador == '1':
            if 'flag_administrador' in data:
                usuario.flag_administrador = data['flag_administrador']
            if 'flag_inventarios' in data:
                usuario.flag_inventarios = data['flag_inventarios']
            if 'flag_estado' in data:
                usuario.flag_estado = data['flag_estado']

        db.session.commit()

        return {"message": "Usuario actualizado exitosamente"}, 200

    @usuario_ns.expect(auth_parser)
    @usuario_ns.response(200, 'Usuario inactivado exitosamente')
    @usuario_ns.response(401, 'Token inválido o faltante')
    @usuario_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @usuario_ns.response(404, 'Usuario no encontrado')
    def delete(self, id_user):
        """Inactivar un usuario (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        usuario = Usuario.query.get(id_user)
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404

        # No permitir inactivarse a sí mismo
        if current_user.id_user == id_user:
            return {"message": "No puede inactivar su propio usuario"}, 400

        usuario.flag_estado = '0'
        db.session.commit()

        return {"message": "Usuario inactivado exitosamente"}, 200

@usuario_ns.route('/<int:id_user>/reactivar')
class ReactivarUsuario(Resource):
    @usuario_ns.expect(auth_parser)
    @usuario_ns.response(200, 'Usuario reactivado exitosamente')
    @usuario_ns.response(401, 'Token inválido o faltante')
    @usuario_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @usuario_ns.response(404, 'Usuario no encontrado')
    def put(self, id_user):
        """Reactivar un usuario inactivo (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        usuario = Usuario.query.get(id_user)
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404

        usuario.flag_estado = '1'
        db.session.commit()

        return {"message": "Usuario reactivado exitosamente"}, 200

@usuario_ns.route('/buscar/<string:nombre>')
class BuscarUsuarios(Resource):
    @usuario_ns.expect(auth_parser)
    @usuario_ns.response(200, 'Búsqueda completada exitosamente')
    @usuario_ns.response(401, 'Token inválido o faltante')
    @usuario_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @usuario_ns.marshal_list_with(usuario_response_model)
    def get(self, nombre):
        """Buscar usuarios por nombre (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        usuarios = Usuario.query.filter(
            Usuario.nombre_user.ilike(f'%{nombre}%'),
            Usuario.flag_estado == '1'
        ).all()
        
        return [usuario.to_dict() for usuario in usuarios], 200

@usuario_ns.route('/administradores')
class UsuariosAdministradores(Resource):
    @usuario_ns.expect(auth_parser)
    @usuario_ns.response(200, 'Administradores obtenidos exitosamente')
    @usuario_ns.response(401, 'Token inválido o faltante')
    @usuario_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @usuario_ns.marshal_list_with(usuario_response_model)
    def get(self):
        """Obtener todos los usuarios administradores (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        usuarios = Usuario.query.filter_by(
            flag_administrador='1', 
            flag_estado='1'
        ).all()
        
        return [usuario.to_dict() for usuario in usuarios], 200

@usuario_ns.route('/inventarios')
class UsuariosConInventarios(Resource):
    @usuario_ns.expect(auth_parser)
    @usuario_ns.response(200, 'Usuarios con permisos de inventario obtenidos exitosamente')
    @usuario_ns.response(401, 'Token inválido o faltante')
    @usuario_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @usuario_ns.marshal_list_with(usuario_response_model)
    def get(self):
        """Obtener usuarios con permisos de inventario (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        usuarios = Usuario.query.filter_by(
            flag_inventarios='1', 
            flag_estado='1'
        ).all()
        
        return [usuario.to_dict() for usuario in usuarios], 200