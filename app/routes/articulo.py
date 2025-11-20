# app/routes/articulo.py
from flask import Blueprint, request, jsonify
from app.models.articulo import Articulo
from app.extensions import db
from app.services.auth_service import generate_token
from app.decorators.PyJWT import token_required

articulo_bp = Blueprint('articulo', __name__)

# Obtener todos los artículos
@articulo_bp.route('/', methods=['GET'])
@token_required
def ConsultarArticulos(current_user):
    articulos = Articulo.query.all()
    output = [articulo.to_dict() for articulo in articulos]

    return jsonify({'articulos': output}), 200

# Obtener un artículo por ID
@articulo_bp.route('/<int:id_articulo>', methods=['GET'])
@token_required
def ConsultarArticuloID(current_user, id_articulo):
    articulo = Articulo.query.get(id_articulo)
    if not articulo:
        return jsonify({"message": "Artículo no encontrado"}), 404

    return jsonify(articulo.to_dict()), 200

# Crear un nuevo artículo (solo para administradores)
@articulo_bp.route('/', methods=['POST'])
@token_required
def CrearArticulo(current_user):
    # if current_user.flag_administrador != '1':
    #     return jsonify({"message": "Acceso denegado"}), 403

    data = request.get_json()
    # ✅ Validar campos obligatorios
    campos_requeridos = ['nombre_articulo', 'cod_articulo', 'cod_unidad', 'id_categoria']
    for campo in campos_requeridos:
        if not data.get(campo):
            return jsonify({"message": f"Falta el campo: {campo}"}), 400

    # ✅ Validar relaciones existan
    from app.models.unidad import Unidad
    from app.models.categoria import Categoria
    
    if not Unidad.query.get(data['cod_unidad']):
        return jsonify({"message": "Unidad de medida no existe"}), 400
        
    if not Categoria.query.get(data['id_categoria']):
        return jsonify({"message": "Categoría no existe"}), 400

    # ✅ Validar código único
    if Articulo.query.filter_by(cod_articulo=data['cod_articulo']).first():
        return jsonify({"message": "Ya existe un artículo con este código"}), 400

    articulo = Articulo(
        cod_articulo=data['cod_articulo'],
        nombre_articulo=data['nombre_articulo'],
        descripcion_articulo=data.get('descripcion_articulo', ''),
        precio_articulo=data.get('precio_articulo', 0.0),
        stock_articulo=data.get('stock_articulo', 0),
        cod_unidad=data['cod_unidad'],
        id_categoria=data['id_categoria']
    )
    
    db.session.add(articulo)
    db.session.commit()

    return jsonify({
        "message": "Artículo creado exitosamente",
        "id_articulo": articulo.id_articulo
    }), 201

# Actualizar un artículo (solo para administradores)
@articulo_bp.route('/<int:id_articulo>', methods=['PUT'])
@token_required
def ActualizarArticulo(current_user, id_articulo):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    articulo = Articulo.query.get(id_articulo)
    if not articulo:
        return jsonify({"message": "Artículo no encontrado"}), 404

    data = request.get_json()
    articulo.nombre_articulo = data.get("nombre_articulo", articulo.nombre_articulo)
    articulo.descripcion_articulo = data.get("descripcion_articulo", articulo.descripcion_articulo)
    articulo.precio_articulo = data.get("precio_articulo", articulo.precio_articulo)
    articulo.stock_articulo = data.get("stock_articulo", articulo.stock_articulo)

    db.session.commit()

    return jsonify({"message": "Artículo actualizado exitosamente"}), 200

# Inactivar un artículo (solo para administradores)
@articulo_bp.route('/<int:id_articulo>', methods=['DELETE'])
@token_required
def InactivarArticulo(current_user, id_articulo):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    articulo = Articulo.query.get(id_articulo)
    if not articulo:
        return jsonify({"message": "Artículo no encontrado"}), 404

    articulo.flag_estado = '0'  # Inactivar el artículo
    db.session.commit()

    return jsonify({"message": "Artículo inactivado exitosamente"}), 200

# Buscar artículos por nombre
@articulo_bp.route('/buscar', methods=['GET'])
@token_required
def BuscarArticulos(current_user):
    nombre = request.args.get('nombre', '')
    articulos = Articulo.query.filter(Articulo.nombre_articulo.ilike(f'%{nombre}%')).all()
    output = [articulo.to_dict() for articulo in articulos]

    return jsonify({'articulos': output}), 200

# Consultar artículos por categoría
@articulo_bp.route('/categoria/<int:id_categoria>', methods=['GET'])
@token_required
def ConsultarArticulosPorCategoria(current_user, id_categoria):
    articulos = Articulo.query.filter_by(id_categoria=id_categoria).all()
    output = [articulo.to_dict() for articulo in articulos]

    return jsonify({'articulos': output}), 200

# Consultar artículos por unidad de medida
@articulo_bp.route('/unidad/<string:cod_unidad>', methods=['GET'])
@token_required
def ConsultarArticulosPorUnidad(current_user, cod_unidad):
    articulos = Articulo.query.filter_by(cod_unidad=cod_unidad).all()
    output = [articulo.to_dict() for articulo in articulos]

    return jsonify({'articulos': output}), 200