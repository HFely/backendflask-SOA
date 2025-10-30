# app/routes/entidad_relacion_docs.py
from flask import request
from flask_restx import Resource, fields, Namespace, reqparse
from app.models.entidad_relacion import EntidadRelacion
from app.extensions import db
from app.decorators.PyJWT import token_required

# Crear namespace para Swagger
entidad_relacion_ns = Namespace('entidades-relaciones', description='Operaciones de gestión de entidades de relación (clientes/proveedores)')

# Modelos para la documentación Swagger
entidad_relacion_model = entidad_relacion_ns.model('EntidadRelacion', {
    'id_entidad': fields.Integer(readOnly=True, description='ID único de la entidad'),
    'nombre_entidad': fields.String(required=True, description='Nombre de la entidad'),
    'id_tipo_doc_ident': fields.Integer(required=True, description='ID del tipo de documento de identidad'),
    'nro_doc_ident': fields.String(required=True, description='Número de documento de identidad'),
    'direccion': fields.String(description='Dirección de la entidad'),
    'telefono': fields.String(description='Teléfono de la entidad'),
    'flag_proveedor': fields.String(description='Indica si es proveedor (1:Sí, 0:No)'),
    'flag_cliente': fields.String(description='Indica si es cliente (1:Sí, 0:No)'),
    'flag_estado': fields.String(description='Estado de la entidad (1:Activo, 0:Inactivo)')
})

entidad_create_model = entidad_relacion_ns.model('CrearEntidadRelacion', {
    'nombre_entidad': fields.String(required=True, description='Nombre de la entidad'),
    'id_tipo_doc_ident': fields.Integer(required=True, description='ID del tipo de documento de identidad'),
    'nro_doc_ident': fields.String(required=True, description='Número de documento de identidad'),
    'direccion': fields.String(description='Dirección de la entidad'),
    'telefono': fields.String(description='Teléfono de la entidad'),
    'flag_proveedor': fields.String(default='0', description='Indica si es proveedor (1:Sí, 0:No)'),
    'flag_cliente': fields.String(default='0', description='Indica si es cliente (1:Sí, 0:No)'),
    'flag_estado': fields.String(default='1', description='Estado de la entidad (1:Activo, 0:Inactivo)')
})

entidad_update_model = entidad_relacion_ns.model('ActualizarEntidadRelacion', {
    'nombre_entidad': fields.String(description='Nombre de la entidad'),
    'id_tipo_doc_ident': fields.Integer(description='ID del tipo de documento de identidad'),
    'nro_doc_ident': fields.String(description='Número de documento de identidad'),
    'direccion': fields.String(description='Dirección de la entidad'),
    'telefono': fields.String(description='Teléfono de la entidad'),
    'flag_proveedor': fields.String(description='Indica si es proveedor (1:Sí, 0:No)'),
    'flag_cliente': fields.String(description='Indica si es cliente (1:Sí, 0:No)'),
    'flag_estado': fields.String(description='Estado de la entidad (1:Activo, 0:Inactivo)')
})

entidad_response_model = entidad_relacion_ns.model('EntidadRelacionResponse', {
    'id_entidad': fields.Integer(description='ID único de la entidad'),
    'nombre_entidad': fields.String(description='Nombre de la entidad'),
    'id_tipo_doc_ident': fields.Integer(description='ID del tipo de documento de identidad'),
    'nro_doc_ident': fields.String(description='Número de documento de identidad'),
    'direccion': fields.String(description='Dirección de la entidad'),
    'telefono': fields.String(description='Teléfono de la entidad'),
    'flag_proveedor': fields.String(description='Indica si es proveedor'),
    'flag_cliente': fields.String(description='Indica si es cliente'),
    'flag_estado': fields.String(description='Estado de la entidad')
})

# Parsers para parámetros de consulta
buscar_parser = reqparse.RequestParser()
buscar_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

tipo_doc_parser = reqparse.RequestParser()
tipo_doc_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

doc_tipo_parser = reqparse.RequestParser()
doc_tipo_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

# Parser para headers de autorización
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

# Endpoints con Swagger Documentation
@entidad_relacion_ns.route('/')
class EntidadRelacionList(Resource):
    @entidad_relacion_ns.expect(auth_parser)
    @entidad_relacion_ns.response(200, 'Lista de entidades obtenida exitosamente')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.marshal_list_with(entidad_response_model)
    def get(self):
        """Obtener todas las entidades de relación activas"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        entidades = EntidadRelacion.query.filter_by(flag_estado='1').all()
        return [entidad.to_dict() for entidad in entidades], 200

    @entidad_relacion_ns.expect(auth_parser, entidad_create_model)
    @entidad_relacion_ns.response(201, 'Entidad creada exitosamente')
    @entidad_relacion_ns.response(400, 'Datos inválidos o entidad ya existe')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    def post(self):
        """Crear una nueva entidad de relación (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        from app.models.usuario import Usuario
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        nombre_entidad = data.get("nombre_entidad")
        id_tipo_doc_ident = data.get("id_tipo_doc_ident")
        nro_doc_ident = data.get("nro_doc_ident")
        direccion = data.get("direccion", "")
        telefono = data.get("telefono", "")
        flag_proveedor = data.get("flag_proveedor", '0')
        flag_cliente = data.get("flag_cliente", '0')
        flag_estado = data.get("flag_estado", '1')

        # Validaciones
        if not all([nombre_entidad, id_tipo_doc_ident, nro_doc_ident]):
            return {"message": "Faltan campos obligatorios: nombre_entidad, id_tipo_doc_ident, nro_doc_ident"}, 400

        # Validar que no exista el mismo nombre
        if EntidadRelacion.query.filter_by(nombre_entidad=nombre_entidad).first():
            return {"message": "El nombre de la entidad ya existe"}, 400

        # Validar que no exista el mismo documento identidad con el mismo tipo
        if EntidadRelacion.query.filter_by(
            nro_doc_ident=nro_doc_ident,
            id_tipo_doc_ident=id_tipo_doc_ident
        ).first():
            return {"message": "Ya existe una entidad con este documento de identidad"}, 400

        entidad = EntidadRelacion(
            nombre_entidad=nombre_entidad,
            id_tipo_doc_ident=id_tipo_doc_ident,
            nro_doc_ident=nro_doc_ident,
            direccion=direccion,
            telefono=telefono,
            flag_proveedor=flag_proveedor,
            flag_cliente=flag_cliente,
            flag_estado=flag_estado
        )
        db.session.add(entidad)
        db.session.commit()

        return {"message": "Entidad de relación creada exitosamente", "id_entidad": entidad.id_entidad}, 201

@entidad_relacion_ns.route('/<int:id_entidad>')
class EntidadRelacionDetail(Resource):
    @entidad_relacion_ns.expect(auth_parser)
    @entidad_relacion_ns.response(200, 'Entidad obtenida exitosamente', entidad_response_model)
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.response(404, 'Entidad no encontrada')
    def get(self, id_entidad):
        """Obtener una entidad de relación por ID"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        entidad = EntidadRelacion.query.get(id_entidad)
        if not entidad or entidad.flag_estado != '1':
            return {"message": "Entidad de relación no encontrada"}, 404

        return entidad.to_dict(), 200

    @entidad_relacion_ns.expect(auth_parser, entidad_update_model)
    @entidad_relacion_ns.response(200, 'Entidad actualizada exitosamente')
    @entidad_relacion_ns.response(400, 'Datos inválidos o conflictos')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @entidad_relacion_ns.response(404, 'Entidad no encontrada')
    def put(self, id_entidad):
        """Actualizar una entidad de relación (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        from app.models.usuario import Usuario
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        entidad = EntidadRelacion.query.get(id_entidad)
        if not entidad:
            return {"message": "Entidad de relación no encontrada"}, 404

        # Validar unicidad del nombre si se está cambiando
        if 'nombre_entidad' in data and data['nombre_entidad'] != entidad.nombre_entidad:
            if EntidadRelacion.query.filter_by(nombre_entidad=data['nombre_entidad']).first():
                return {"message": "El nombre de la entidad ya existe"}, 400

        # Validar unicidad del documento si se está cambiando
        if ('nro_doc_ident' in data and data['nro_doc_ident'] != entidad.nro_doc_ident) or \
           ('id_tipo_doc_ident' in data and data['id_tipo_doc_ident'] != entidad.id_tipo_doc_ident):
            
            nro_doc = data.get('nro_doc_ident', entidad.nro_doc_ident)
            tipo_doc = data.get('id_tipo_doc_ident', entidad.id_tipo_doc_ident)
            
            existing = EntidadRelacion.query.filter(
                EntidadRelacion.nro_doc_ident == nro_doc,
                EntidadRelacion.id_tipo_doc_ident == tipo_doc,
                EntidadRelacion.id_entidad != id_entidad
            ).first()
            
            if existing:
                return {"message": "Ya existe otra entidad con este documento de identidad"}, 400

        # Actualizar campos
        campos = ['nombre_entidad', 'id_tipo_doc_ident', 'nro_doc_ident', 'direccion', 
                  'telefono', 'flag_proveedor', 'flag_cliente', 'flag_estado']
        
        for campo in campos:
            if campo in data:
                setattr(entidad, campo, data[campo])

        db.session.commit()

        return {"message": "Entidad de relación actualizada exitosamente"}, 200

    @entidad_relacion_ns.expect(auth_parser)
    @entidad_relacion_ns.response(200, 'Entidad inactivada exitosamente')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @entidad_relacion_ns.response(404, 'Entidad no encontrada')
    def delete(self, id_entidad):
        """Inactivar una entidad de relación (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        from app.models.usuario import Usuario
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        entidad = EntidadRelacion.query.get(id_entidad)
        if not entidad:
            return {"message": "Entidad de relación no encontrada"}, 404

        entidad.flag_estado = '0'
        db.session.commit()

        return {"message": "Entidad de relación inactivada exitosamente"}, 200

@entidad_relacion_ns.route('/tipo-doc/<int:id_tipo_doc>')
class EntidadesPorTipoDoc(Resource):
    @entidad_relacion_ns.expect(tipo_doc_parser)
    @entidad_relacion_ns.response(200, 'Entidades obtenidas exitosamente')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.marshal_list_with(entidad_response_model)
    def get(self, id_tipo_doc):
        """Obtener entidades por tipo de documento de identidad"""
        args = tipo_doc_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        entidades = EntidadRelacion.query.filter_by(
            id_tipo_doc_ident=id_tipo_doc, 
            flag_estado='1'
        ).all()
        
        return [entidad.to_dict() for entidad in entidades], 200

@entidad_relacion_ns.route('/doc/<string:nro_doc_ident>/tipo-doc/<int:id_tipo_doc>')
class EntidadesPorDocYTipo(Resource):
    @entidad_relacion_ns.expect(doc_tipo_parser)
    @entidad_relacion_ns.response(200, 'Entidades obtenidas exitosamente')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.marshal_list_with(entidad_response_model)
    def get(self, nro_doc_ident, id_tipo_doc):
        """Obtener entidades por número y tipo de documento de identidad"""
        args = doc_tipo_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        entidades = EntidadRelacion.query.filter_by(
            nro_doc_ident=nro_doc_ident,
            id_tipo_doc_ident=id_tipo_doc,
            flag_estado='1'
        ).all()
        
        return [entidad.to_dict() for entidad in entidades], 200

@entidad_relacion_ns.route('/buscar/<string:nombre>')
class BuscarEntidadesPorNombre(Resource):
    @entidad_relacion_ns.expect(buscar_parser)
    @entidad_relacion_ns.response(200, 'Búsqueda completada exitosamente')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.marshal_list_with(entidad_response_model)
    def get(self, nombre):
        """Buscar entidades por nombre (búsqueda parcial)"""
        args = buscar_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        entidades = EntidadRelacion.query.filter(
            EntidadRelacion.nombre_entidad.ilike(f'%{nombre}%'),
            EntidadRelacion.flag_estado == '1'
        ).all()
        
        return [entidad.to_dict() for entidad in entidades], 200

@entidad_relacion_ns.route('/proveedores')
class EntidadesProveedores(Resource):
    @entidad_relacion_ns.expect(auth_parser)
    @entidad_relacion_ns.response(200, 'Proveedores obtenidos exitosamente')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.marshal_list_with(entidad_response_model)
    def get(self):
        """Obtener todas las entidades que son proveedores"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        entidades = EntidadRelacion.query.filter_by(
            flag_proveedor='1', 
            flag_estado='1'
        ).all()
        
        return [entidad.to_dict() for entidad in entidades], 200

@entidad_relacion_ns.route('/clientes')
class EntidadesClientes(Resource):
    @entidad_relacion_ns.expect(auth_parser)
    @entidad_relacion_ns.response(200, 'Clientes obtenidos exitosamente')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.marshal_list_with(entidad_response_model)
    def get(self):
        """Obtener todas las entidades que son clientes"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        entidades = EntidadRelacion.query.filter_by(
            flag_cliente='1', 
            flag_estado='1'
        ).all()
        
        return [entidad.to_dict() for entidad in entidades], 200

@entidad_relacion_ns.route('/<int:id_entidad>/reactivar')
class ReactivarEntidad(Resource):
    @entidad_relacion_ns.expect(auth_parser)
    @entidad_relacion_ns.response(200, 'Entidad reactivada exitosamente')
    @entidad_relacion_ns.response(401, 'Token inválido o faltante')
    @entidad_relacion_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @entidad_relacion_ns.response(404, 'Entidad no encontrada')
    def put(self, id_entidad):
        """Reactivar una entidad inactiva (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        from app.models.usuario import Usuario
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_administrador != '1':
            return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        entidad = EntidadRelacion.query.get(id_entidad)
        if not entidad:
            return {"message": "Entidad de relación no encontrada"}, 404

        entidad.flag_estado = '1'
        db.session.commit()

        return {"message": "Entidad de relación reactivada exitosamente"}, 200