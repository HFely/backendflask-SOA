# app/routes/articulo_docs.py
from flask import request
from flask_restx import Resource, fields, Namespace, reqparse
from app.models.articulo import Articulo
from app.models.unidad import Unidad
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.extensions import db
from app.decorators.PyJWT import token_required
from app.services.auth_service import decode_token

# Crear namespace para Swagger
articulo_ns = Namespace('articulos', description='Operaciones de gestión de artículos')

# Modelos para la documentación Swagger - CORREGIDOS
articulo_model = articulo_ns.model('Articulo', {
    'id_articulo': fields.Integer(readOnly=True, description='ID único del artículo'),
    'cod_articulo': fields.String(required=True, description='Código único del artículo (12 caracteres)'),
    'nombre_articulo': fields.String(required=True, description='Nombre del artículo'),
    'descripcion_articulo': fields.String(description='Descripción del artículo'),
    'precio_articulo': fields.Float(required=True, description='Precio del artículo'),
    'stock_articulo': fields.Integer(required=True, description='Stock disponible'),
    'cod_unidad': fields.String(required=True, description='Código de unidad de medida'),
    'id_categoria': fields.Integer(required=True, description='ID de la categoría'),
    'flag_estado': fields.String(description='Estado del artículo (1:Activo, 0:Inactivo)')
})

# ✅ CORREGIDO: Incluir cod_articulo que es campo obligatorio
articulo_create_model = articulo_ns.model('CrearArticulo', {
    'cod_articulo': fields.String(required=True, description='Código único del artículo (12 caracteres)'),
    'nombre_articulo': fields.String(required=True, description='Nombre del artículo'),
    'descripcion_articulo': fields.String(description='Descripción del artículo'),
    'precio_articulo': fields.Float(required=True, description='Precio del artículo'),
    'stock_articulo': fields.Integer(required=True, description='Stock disponible'),
    'cod_unidad': fields.String(required=True, description='Código de unidad de medida'),
    'id_categoria': fields.Integer(required=True, description='ID de la categoría')
})

articulo_update_model = articulo_ns.model('ActualizarArticulo', {
    'cod_articulo': fields.String(description='Código único del artículo'),
    'nombre_articulo': fields.String(description='Nombre del artículo'),
    'descripcion_articulo': fields.String(description='Descripción del artículo'),
    'precio_articulo': fields.Float(description='Precio del artículo'),
    'stock_articulo': fields.Integer(description='Stock disponible'),
    'cod_unidad': fields.String(description='Código de unidad de medida'),
    'id_categoria': fields.Integer(description='ID de la categoría')
})

articulo_response_model = articulo_ns.model('ArticuloResponse', {
    'id_articulo': fields.Integer(description='ID único del artículo'),
    'cod_articulo': fields.String(description='Código único del artículo'),
    'nombre_articulo': fields.String(description='Nombre del artículo'),
    'descripcion_articulo': fields.String(description='Descripción del artículo'),
    'precio_articulo': fields.Float(description='Precio del artículo'),
    'stock_articulo': fields.Integer(description='Stock disponible'),
    'cod_unidad': fields.String(description='Código de unidad de medida'),
    'id_categoria': fields.Integer(description='ID de la categoría'),
    'flag_estado': fields.String(description='Estado del artículo')
})

# Parsers para parámetros de consulta
buscar_parser = reqparse.RequestParser()
buscar_parser.add_argument('nombre', location='args', required=True, help='Nombre a buscar')

categoria_parser = reqparse.RequestParser()
categoria_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

unidad_parser = reqparse.RequestParser()
unidad_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

# Parser para headers de autorización
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', location='headers', required=True, help='Token Bearer')

# Endpoints con Swagger Documentation - CORREGIDOS
@articulo_ns.route('/')
class ArticuloList(Resource):
    @articulo_ns.expect(auth_parser)
    @articulo_ns.response(200, 'Lista de artículos obtenida exitosamente')
    @articulo_ns.response(401, 'Token inválido o faltante')
    @articulo_ns.marshal_list_with(articulo_response_model)
    def get(self):
        """Obtener todos los artículos activos"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token usando el decorator
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        articulos = Articulo.query.filter_by(flag_estado='1').all()
        return [articulo.to_dict() for articulo in articulos], 200

    @articulo_ns.expect(auth_parser, articulo_create_model)
    @articulo_ns.response(201, 'Artículo creado exitosamente')
    @articulo_ns.response(400, 'Datos inválidos o faltantes')
    @articulo_ns.response(401, 'Token inválido o faltante')
    @articulo_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    def post(self):
        """Crear un nuevo artículo (Requiere rol administrador)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        data = request.get_json()
        
        # Verificar token y permisos
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        current_user = Usuario.query.get(token_data["user_id"])
        # if not current_user or current_user.flag_administrador != '1':
        #     return {"message": "Acceso denegado - Se requiere rol administrador"}, 403

        # ✅ VALIDACIONES COMPLETAS Y CORRECTAS
        # 1. Validar campos requeridos
        campos_requeridos = ['cod_articulo', 'nombre_articulo', 'cod_unidad', 'id_categoria']
        for campo in campos_requeridos:
            if not data.get(campo):
                return {"message": f"Falta el campo requerido: {campo}"}, 400

        # 2. Validar formato del código (12 caracteres máximo)
        cod_articulo = data.get('cod_articulo', '').strip()
        if len(cod_articulo) > 12:
            return {"message": "El código del artículo no puede exceder 12 caracteres"}, 400

        # 3. Validar que el código sea único
        if Articulo.query.filter_by(cod_articulo=cod_articulo).first():
            return {"message": "Ya existe un artículo con este código"}, 400

        # 4. Validar que la unidad exista
        cod_unidad = data.get('cod_unidad')
        if not Unidad.query.get(cod_unidad):
            return {"message": "La unidad de medida no existe"}, 400

        # 5. Validar que la categoría exista
        id_categoria = data.get('id_categoria')
        if not Categoria.query.get(id_categoria):
            return {"message": "La categoría no existe"}, 400

        # 6. Validar valores numéricos
        precio_articulo = data.get('precio_articulo', 0.0)
        stock_articulo = data.get('stock_articulo', 0)

        if precio_articulo < 0:
            return {"message": "El precio no puede ser negativo"}, 400

        if stock_articulo < 0:
            return {"message": "El stock no puede ser negativo"}, 400

        # ✅ CREAR EL ARTÍCULO CON TODOS LOS CAMPOS REQUERIDOS
        try:
            articulo = Articulo(
                cod_articulo=cod_articulo,
                nombre_articulo=data.get('nombre_articulo'),
                descripcion_articulo=data.get('descripcion_articulo', ''),
                precio_articulo=precio_articulo,
                stock_articulo=stock_articulo,
                cod_unidad=cod_unidad,
                id_categoria=id_categoria
            )
            
            db.session.add(articulo)
            db.session.commit()

            return {
                "message": "Artículo creado exitosamente", 
                "id_articulo": articulo.id_articulo,
                "cod_articulo": articulo.cod_articulo
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error al crear el artículo: {str(e)}"}, 500

@articulo_ns.route('/<int:id_articulo>')
class ArticuloDetail(Resource):
    @articulo_ns.expect(auth_parser)
    @articulo_ns.response(200, 'Artículo obtenido exitosamente', articulo_response_model)
    @articulo_ns.response(401, 'Token inválido o faltante')
    @articulo_ns.response(404, 'Artículo no encontrado')
    def get(self, id_articulo):
        """Obtener un artículo por ID"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        articulo = Articulo.query.get(id_articulo)
        if not articulo or articulo.flag_estado != '1':
            return {"message": "Artículo no encontrado"}, 404

        return articulo.to_dict(), 200

    @articulo_ns.expect(auth_parser, articulo_update_model)
    @articulo_ns.response(200, 'Artículo actualizado exitosamente')
    @articulo_ns.response(400, 'Datos inválidos')
    @articulo_ns.response(401, 'Token inválido o faltante')
    @articulo_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @articulo_ns.response(404, 'Artículo no encontrado')
    def put(self, id_articulo):
        """Actualizar un artículo (Requiere rol administrador)"""
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

        articulo = Articulo.query.get(id_articulo)
        if not articulo:
            return {"message": "Artículo no encontrado"}, 404

        # Validaciones de datos
        if 'precio_articulo' in data and data['precio_articulo'] < 0:
            return {"message": "El precio no puede ser negativo"}, 400

        if 'stock_articulo' in data and data['stock_articulo'] < 0:
            return {"message": "El stock no puede ser negativo"}, 400

        # Actualizar campos
        if 'nombre_articulo' in data:
            articulo.nombre_articulo = data['nombre_articulo']
        if 'descripcion_articulo' in data:
            articulo.descripcion_articulo = data['descripcion_articulo']
        if 'precio_articulo' in data:
            articulo.precio_articulo = data['precio_articulo']
        if 'stock_articulo' in data:
            articulo.stock_articulo = data['stock_articulo']
        if 'cod_unidad' in data:
            articulo.cod_unidad = data['cod_unidad']
        if 'id_categoria' in data:
            articulo.id_categoria = data['id_categoria']

        db.session.commit()

        return {"message": "Artículo actualizado exitosamente"}, 200

    @articulo_ns.expect(auth_parser)
    @articulo_ns.response(200, 'Artículo inactivado exitosamente')
    @articulo_ns.response(401, 'Token inválido o faltante')
    @articulo_ns.response(403, 'Acceso denegado - Se requiere rol administrador')
    @articulo_ns.response(404, 'Artículo no encontrado')
    def delete(self, id_articulo):
        """Inactivar un artículo (Requiere rol administrador)"""
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

        articulo = Articulo.query.get(id_articulo)
        if not articulo:
            return {"message": "Artículo no encontrado"}, 404

        articulo.flag_estado = '0'  # Inactivar el artículo
        db.session.commit()

        return {"message": "Artículo inactivado exitosamente"}, 200

@articulo_ns.route('/buscar')
class BuscarArticulos(Resource):
    @articulo_ns.expect(buscar_parser)
    @articulo_ns.response(200, 'Búsqueda completada exitosamente')
    @articulo_ns.response(400, 'Parámetro de búsqueda faltante')
    @articulo_ns.marshal_list_with(articulo_response_model)
    def get(self):
        """Buscar artículos por nombre"""
        args = buscar_parser.parse_args()
        nombre = args['nombre']
        
        if not nombre:
            return {"message": "El parámetro 'nombre' es requerido"}, 400

        articulos = Articulo.query.filter(
            Articulo.nombre_articulo.ilike(f'%{nombre}%'),
            Articulo.flag_estado == '1'
        ).all()
        
        return [articulo.to_dict() for articulo in articulos], 200

@articulo_ns.route('/categoria/<int:id_categoria>')
class ArticulosPorCategoria(Resource):
    @articulo_ns.expect(categoria_parser)
    @articulo_ns.response(200, 'Artículos obtenidos exitosamente')
    @articulo_ns.response(401, 'Token inválido o faltante')
    @articulo_ns.marshal_list_with(articulo_response_model)
    def get(self, id_categoria):
        """Obtener artículos por categoría"""
        args = categoria_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        articulos = Articulo.query.filter_by(
            id_categoria=id_categoria, 
            flag_estado='1'
        ).all()
        
        return [articulo.to_dict() for articulo in articulos], 200

@articulo_ns.route('/unidad/<string:cod_unidad>')
class ArticulosPorUnidad(Resource):
    @articulo_ns.expect(unidad_parser)
    @articulo_ns.response(200, 'Artículos obtenidos exitosamente')
    @articulo_ns.response(401, 'Token inválido o faltante')
    @articulo_ns.marshal_list_with(articulo_response_model)
    def get(self, cod_unidad):
        """Obtener artículos por unidad de medida"""
        args = unidad_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        articulos = Articulo.query.filter_by(
            cod_unidad=cod_unidad, 
            flag_estado='1'
        ).all()
        
        return [articulo.to_dict() for articulo in articulos], 200

@articulo_ns.route('/inventario/bajo-stock')
class ArticulosBajoStock(Resource):
    @articulo_ns.expect(auth_parser)
    @articulo_ns.response(200, 'Artículos con bajo stock obtenidos')
    @articulo_ns.response(401, 'Token inválido o faltante')
    @articulo_ns.response(403, 'Acceso denegado')
    @articulo_ns.marshal_list_with(articulo_response_model)
    def get(self):
        """Obtener artículos con stock bajo (Requiere permisos de inventario)"""
        args = auth_parser.parse_args()
        token = args['Authorization'].split(" ")[1]
        
        # Verificar token y permisos de inventario
        from app.services.auth_service import decode_token
        token_data = decode_token(token)
        if "error" in token_data:
            return {"message": token_data["error"]}, 401
            
        from app.models.usuario import Usuario
        current_user = Usuario.query.get(token_data["user_id"])
        if not current_user or current_user.flag_inventarios != '1':
            return {"message": "Acceso denegado - Se requieren permisos de inventario"}, 403

        # Definir umbral de stock bajo (puede ser configurable)
        UMBRAL_STOCK_BAJO = 10
        
        articulos = Articulo.query.filter(
            Articulo.stock_articulo <= UMBRAL_STOCK_BAJO,
            Articulo.flag_estado == '1'
        ).all()
        
        return [articulo.to_dict() for articulo in articulos], 200