from flask import request
from flask_restx import Resource, fields, Namespace, reqparse
from app.models.usuario import Usuario
from app.models.vale_almacen import ValeAlmacen
from app.models.vale_almacen_det import ValeAlmacenDet
from app.extensions import db
from datetime import datetime

# Crear namespace para Swagger
vale_almacen_ns = Namespace('vales-almacen', description='Operaciones de gestión de vales de almacén')

# Modelos para la documentación Swagger
vale_almacen_model = vale_almacen_ns.model('ValeAlmacen', {
    'id_vale_almacen': fields.Integer(readOnly=True, description='ID único del vale'),
    'cod_vale_almacen': fields.String(required=True, description='Código único del vale'),
    'id_almacen': fields.Integer(required=True, description='ID del almacén'),
    'fecha_vale': fields.Date(required=True, description='Fecha del vale (YYYY-MM-DD)'),
    'fecha_registro': fields.DateTime(readOnly=True, description='Fecha de registro del vale'),
    'id_tipo_mov_almacen': fields.Integer(required=True, description='ID del tipo de movimiento'),
    'id_user': fields.Integer(required=True, description='ID del usuario que creó el vale'),
    'id_entidad': fields.Integer(description='ID de la entidad (cliente/proveedor)'),
    'id_tipo_doc': fields.Integer(description='ID del tipo de documento'),
    'serie_doc': fields.String(description='Serie del documento'),
    'nro_documento': fields.String(description='Número del documento'),
    'flag_estado': fields.String(description='Estado del vale (1:Activo, 0:Inactivo)')
})

vale_almacen_create_model = vale_almacen_ns.model('CrearValeAlmacen', {
    'cod_vale_almacen': fields.String(required=True, description='Código único del vale'),
    'id_almacen': fields.Integer(required=True, description='ID del almacén'),
    'fecha_vale': fields.Date(description='Fecha del vale (YYYY-MM-DD) - Opcional, por defecto hoy'),
    'id_tipo_mov_almacen': fields.Integer(required=True, description='ID del tipo de movimiento'),
    'id_user': fields.Integer(required=True, description='ID del usuario que crea el vale'),
    'id_entidad': fields.Integer(description='ID de la entidad (cliente/proveedor)'),
    'id_tipo_doc': fields.Integer(description='ID del tipo de documento'),
    'serie_doc': fields.String(description='Serie del documento'),
    'nro_documento': fields.String(description='Número del documento'),
    'flag_estado': fields.String(default='1', description='Estado del vale')
})

vale_almacen_update_model = vale_almacen_ns.model('ActualizarValeAlmacen', {
    'cod_vale_almacen': fields.String(description='Código único del vale'),
    'id_almacen': fields.Integer(description='ID del almacén'),
    'fecha_vale': fields.Date(description='Fecha del vale (YYYY-MM-DD)'),
    'id_tipo_mov_almacen': fields.Integer(description='ID del tipo de movimiento'),
    'id_user': fields.Integer(description='ID del usuario'),
    'id_entidad': fields.Integer(description='ID de la entidad (cliente/proveedor)'),
    'id_tipo_doc': fields.Integer(description='ID del tipo de documento'),
    'serie_doc': fields.String(description='Serie del documento'),
    'nro_documento': fields.String(description='Número del documento'),
    'flag_estado': fields.String(description='Estado del vale')
})

detalle_vale_model = vale_almacen_ns.model('DetalleValeAlmacen', {
    'id_articulo': fields.Integer(required=True, description='ID del artículo'),
    'cantidad': fields.Float(required=True, description='Cantidad del artículo'),
    'precio_soles': fields.Float(required=True, description='Precio unitario en soles'),
    'item': fields.Integer(description='Número de item (opcional)')
})

detalles_vale_create_model = vale_almacen_ns.model('CrearDetallesVale', {
    'detalles': fields.List(fields.Nested(detalle_vale_model), required=True, description='Lista de detalles del vale')
})

vale_almacen_response_model = vale_almacen_ns.model('ValeAlmacenResponse', {
    'id_vale_almacen': fields.Integer(description='ID único del vale'),
    'cod_vale_almacen': fields.String(description='Código único del vale'),
    'id_almacen': fields.Integer(description='ID del almacén'),
    'fecha_vale': fields.Date(description='Fecha del vale'),
    'fecha_registro': fields.DateTime(description='Fecha de registro'),
    'id_tipo_mov_almacen': fields.Integer(description='ID del tipo de movimiento'),
    'id_user': fields.Integer(description='ID del usuario'),
    'id_entidad': fields.Integer(description='ID de la entidad'),
    'id_tipo_doc': fields.Integer(description='ID del tipo de documento'),
    'serie_doc': fields.String(description='Serie del documento'),
    'nro_documento': fields.String(description='Número del documento'),
    'flag_estado': fields.String(description='Estado del vale')
})

detalle_response_model = vale_almacen_ns.model('DetalleValeResponse', {
    'id_detalle_vale': fields.Integer(description='ID del detalle'),
    'id_vale_almacen': fields.Integer(description='ID del vale'),
    'id_articulo': fields.Integer(description='ID del artículo'),
    'cantidad': fields.Float(description='Cantidad'),
    'precio_soles': fields.Float(description='Precio unitario'),
    'item': fields.Integer(description='Número de item'),
    'flag_estado': fields.String(description='Estado del detalle')
})

# Parsers para parámetros de consulta
fecha_parser = reqparse.RequestParser()
fecha_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

tipo_mov_parser = reqparse.RequestParser()
tipo_mov_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

tipo_doc_parser = reqparse.RequestParser()
tipo_doc_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

usuario_parser = reqparse.RequestParser()
usuario_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

entidad_parser = reqparse.RequestParser()
entidad_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

almacen_parser = reqparse.RequestParser()
almacen_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

# Parser para headers de autorización
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

# Endpoints con Swagger Documentation
@vale_almacen_ns.route('/')
class ValeAlmacenList(Resource):
    @vale_almacen_ns.expect(auth_parser)
    @vale_almacen_ns.response(200, 'Lista de vales obtenida exitosamente')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.marshal_list_with(vale_almacen_response_model)
    def get(self):
        """Obtener todos los vales de almacén activos"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        vales = ValeAlmacen.query.filter_by(flag_estado='1').all()
        return [vale.to_dict() for vale in vales], 200

    @vale_almacen_ns.expect(auth_parser, vale_almacen_create_model)
    @vale_almacen_ns.response(201, 'Vale de almacén creado exitosamente')
    @vale_almacen_ns.response(400, 'Datos inválidos o código ya existe')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    def post(self):
        """Crear un nuevo vale de almacén"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401

        # Validar campos obligatorios
        required_fields = ['cod_vale_almacen', 'id_almacen', 'id_tipo_mov_almacen', 'id_user']
        if not all(field in data for field in required_fields):
            return {"message": "Datos incompletos para crear el vale de almacén"}, 400

        # Verificar si el código ya existe
        if ValeAlmacen.query.filter_by(cod_vale_almacen=data['cod_vale_almacen']).first():
            return {"message": "El código de vale ya existe"}, 400

        # Procesar fecha
        fecha_vale = data.get('fecha_vale')
        if fecha_vale:
            try:
                fecha_vale = datetime.strptime(fecha_vale, '%Y-%m-%d')
            except ValueError:
                return {"message": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400
        else:
            fecha_vale = datetime.utcnow()

        nuevo_vale = ValeAlmacen(
            cod_vale_almacen=data['cod_vale_almacen'],
            id_almacen=data['id_almacen'],
            fecha_vale=fecha_vale,
            fecha_registro=datetime.utcnow(),
            id_tipo_mov_almacen=data['id_tipo_mov_almacen'],
            id_user=data['id_user'],
            id_entidad=data.get('id_entidad'),
            id_tipo_doc=data.get('id_tipo_doc'),
            serie_doc=data.get('serie_doc'),
            nro_documento=data.get('nro_documento'),
            flag_estado=data.get('flag_estado', '1')
        )

        db.session.add(nuevo_vale)
        db.session.commit()

        return {
            "message": "Vale de almacén creado exitosamente", 
            "id_vale_almacen": nuevo_vale.id_vale_almacen
        }, 201

@vale_almacen_ns.route('/<int:id_vale>')
class ValeAlmacenDetail(Resource):
    @vale_almacen_ns.expect(auth_parser)
    @vale_almacen_ns.response(200, 'Vale obtenido exitosamente', vale_almacen_response_model)
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.response(404, 'Vale no encontrado')
    def get(self, id_vale):
        """Obtener un vale de almacén por ID"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        vale = ValeAlmacen.query.get(id_vale)
        if not vale or vale.flag_estado != '1':
            return {"message": "Vale de almacén no encontrado"}, 404

        return vale.to_dict(), 200

    @vale_almacen_ns.expect(auth_parser, vale_almacen_update_model)
    @vale_almacen_ns.response(200, 'Vale actualizado exitosamente')
    @vale_almacen_ns.response(400, 'Datos inválidos')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.response(404, 'Vale no encontrado')
    def put(self, id_vale):
        """Modificar un vale de almacén"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        vale = ValeAlmacen.query.get(id_vale)
        if not vale:
            return {"message": "Vale de almacén no encontrado"}, 404

        # Actualizar campos
        if 'cod_vale_almacen' in data:
            vale.cod_vale_almacen = data['cod_vale_almacen']
        if 'id_almacen' in data:
            vale.id_almacen = data['id_almacen']
        if 'fecha_vale' in data:
            try:
                vale.fecha_vale = datetime.strptime(data['fecha_vale'], '%Y-%m-%d')
            except ValueError:
                return {"message": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400
        if 'id_tipo_mov_almacen' in data:
            vale.id_tipo_mov_almacen = data['id_tipo_mov_almacen']
        if 'id_user' in data:
            vale.id_user = data['id_user']
        if 'id_entidad' in data:
            vale.id_entidad = data['id_entidad']
        if 'id_tipo_doc' in data:
            vale.id_tipo_doc = data['id_tipo_doc']
        if 'serie_doc' in data:
            vale.serie_doc = data['serie_doc']
        if 'nro_documento' in data:
            vale.nro_documento = data['nro_documento']
        if 'flag_estado' in data:
            vale.flag_estado = data['flag_estado']

        db.session.commit()

        return {"message": "Vale de almacén modificado exitosamente"}, 200

    @vale_almacen_ns.expect(auth_parser)
    @vale_almacen_ns.response(200, 'Vale inactivado exitosamente')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.response(404, 'Vale no encontrado')
    def delete(self, id_vale):
        """Inactivar un vale de almacén y sus detalles"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        vale = ValeAlmacen.query.get(id_vale)
        if not vale:
            return {"message": "Vale de almacén no encontrado"}, 404

        vale.flag_estado = '0'
        # Inactivar también los detalles
        for detalle in vale.detalles:
            detalle.flag_estado = '0'

        db.session.commit()

        return {"message": "Vale de almacén y sus detalles inactivados exitosamente"}, 200

@vale_almacen_ns.route('/<int:id_vale>/detalles')
class DetallesValeAlmacen(Resource):
    @vale_almacen_ns.expect(auth_parser)
    @vale_almacen_ns.response(200, 'Detalles obtenidos exitosamente')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.response(404, 'Vale no encontrado')
    @vale_almacen_ns.marshal_list_with(detalle_response_model)
    def get(self, id_vale):
        """Obtener los detalles de un vale de almacén"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        vale = ValeAlmacen.query.get(id_vale)
        if not vale:
            return {"message": "Vale de almacén no encontrado"}, 404

        detalles = [detalle.to_dict() for detalle in vale.detalles if detalle.flag_estado == '1']
        return detalles, 200

    @vale_almacen_ns.expect(auth_parser, detalles_vale_create_model)
    @vale_almacen_ns.response(201, 'Detalles agregados exitosamente')
    @vale_almacen_ns.response(400, 'Datos inválidos o incompletos')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.response(404, 'Vale no encontrado')
    def post(self, id_vale):
        """Agregar detalles a un vale de almacén"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        vale = ValeAlmacen.query.get(id_vale)
        if not vale:
            return {"message": "Vale de almacén no encontrado"}, 404

        if not data or 'detalles' not in data or not isinstance(data['detalles'], list):
            return {"message": "Datos incompletos para agregar detalles"}, 400

        for detalle_data in data['detalles']:
            if 'id_articulo' not in detalle_data or 'cantidad' not in detalle_data or 'precio_soles' not in detalle_data:
                return {"message": "Datos incompletos en uno de los detalles"}, 400

            nuevo_detalle = ValeAlmacenDet(
                id_vale_almacen=id_vale,
                id_articulo=detalle_data['id_articulo'],
                cantidad=detalle_data['cantidad'],
                precio_soles=detalle_data['precio_soles'],
                item=detalle_data.get('item')
            )
            db.session.add(nuevo_detalle)

        db.session.commit()

        return {"message": "Detalles agregados exitosamente al vale de almacén"}, 201

# Endpoints de consulta especializados
@vale_almacen_ns.route('/tipo-mov/<int:id_tipo_mov>/fecha-inicio/<string:fecha_inicio>/fecha-fin/<string:fecha_fin>')
class ValesPorTipoMovimiento(Resource):
    @vale_almacen_ns.expect(tipo_mov_parser)
    @vale_almacen_ns.response(200, 'Vales obtenidos exitosamente')
    @vale_almacen_ns.response(400, 'Formato de fecha inválido')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.marshal_list_with(vale_almacen_response_model)
    def get(self, id_tipo_mov, fecha_inicio, fecha_fin):
        """Consultar vales por tipo de movimiento y rango de fechas"""
        args = tipo_mov_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401

        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            return {"message": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400

        vales = ValeAlmacen.query.filter(
            ValeAlmacen.id_tipo_mov_almacen == id_tipo_mov,
            ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt),
            ValeAlmacen.flag_estado == '1'
        ).all()
        
        return [vale.to_dict() for vale in vales], 200

@vale_almacen_ns.route('/tipo-doc/<int:id_tipo_doc>/nro-doc/<string:nro_doc>/fecha-inicio/<string:fecha_inicio>/fecha-fin/<string:fecha_fin>')
class ValesPorTipoDocNroDoc(Resource):
    @vale_almacen_ns.expect(tipo_doc_parser)
    @vale_almacen_ns.response(200, 'Vales obtenidos exitosamente')
    @vale_almacen_ns.response(400, 'Formato de fecha inválido')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.marshal_list_with(vale_almacen_response_model)
    def get(self, id_tipo_doc, nro_doc, fecha_inicio, fecha_fin):
        """Consultar vales por tipo de documento, número de documento y rango de fechas"""
        args = tipo_doc_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401

        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            return {"message": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400

        vales = ValeAlmacen.query.filter(
            ValeAlmacen.id_tipo_doc == id_tipo_doc,
            ValeAlmacen.nro_documento == nro_doc,
            ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt),
            ValeAlmacen.flag_estado == '1'
        ).all()
        
        return [vale.to_dict() for vale in vales], 200

@vale_almacen_ns.route('/fecha-inicio/<string:fecha_inicio>/fecha-fin/<string:fecha_fin>')
class ValesPorRangoFechas(Resource):
    @vale_almacen_ns.expect(fecha_parser)
    @vale_almacen_ns.response(200, 'Vales obtenidos exitosamente')
    @vale_almacen_ns.response(400, 'Formato de fecha inválido')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.marshal_list_with(vale_almacen_response_model)
    def get(self, fecha_inicio, fecha_fin):
        """Consultar vales por rango de fechas"""
        args = fecha_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401

        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            return {"message": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400

        vales = ValeAlmacen.query.filter(
            ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt),
            ValeAlmacen.flag_estado == '1'
        ).all()
        
        return [vale.to_dict() for vale in vales], 200

@vale_almacen_ns.route('/usuario/<string:usuario>/fecha-inicio/<string:fecha_inicio>/fecha-fin/<string:fecha_fin>')
class ValesPorUsuario(Resource):
    @vale_almacen_ns.expect(usuario_parser)
    @vale_almacen_ns.response(200, 'Vales obtenidos exitosamente')
    @vale_almacen_ns.response(400, 'Formato de fecha inválido')
    @vale_almacen_ns.response(401, 'Token inválido o faltante')
    @vale_almacen_ns.marshal_list_with(vale_almacen_response_model)
    def get(self, usuario, fecha_inicio, fecha_fin):
        """Buscar vales por nombre de usuario y rango de fechas"""
        args = usuario_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401

        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            return {"message": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400

        vales = ValeAlmacen.query.join(Usuario).filter(
            Usuario.nombre_user.ilike(f'%{usuario}%'),
            ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt),
            ValeAlmacen.flag_estado == '1'
        ).all()
        
        return [vale.to_dict() for vale in vales], 200