# app/routes/vale_almacen.py
from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.models.vale_almacen import ValeAlmacen
from app.extensions import db
from app.models.vale_almacen_det import ValeAlmacenDet
from app.services.auth_service import generate_token
from app.decorators.PyJWT import token_required
from datetime import datetime

vale_almacen_bp = Blueprint('vale_almacen', __name__)

# Obtener todos los vales de almacén
@vale_almacen_bp.route('/vales_almacen', methods=['GET'])
@token_required
def ConsultarValesAlmacen(current_user):
    vales = ValeAlmacen.query.all()
    output = [vale.to_dict() for vale in vales]

    return jsonify({'vales_almacen': output}), 200

# Obtener un vale de almacén por ID
@vale_almacen_bp.route('/vales_almacen/<int:id_vale>', methods=['GET'])
@token_required
def ConsultarValeAlmacenID(current_user, id_vale):
    vale = ValeAlmacen.query.get(id_vale)
    if not vale:
        return jsonify({"message": "Vale de almacén no encontrado"}), 404

    return jsonify(vale.to_dict()), 200

# Consultar vales por tipo movimiento de almacen y fecha inicio y fin
@vale_almacen_bp.route('/vales_almacen/tipo_mov/<int:id_tipo_mov>/fecha_inicio/<string:fecha_inicio>/fecha_fin/<string:fecha_fin>', methods=['GET'])
@token_required
def ConsultarValesTipoMovFecha(current_user, id_tipo_mov, fecha_inicio, fecha_fin):
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400

    vales = ValeAlmacen.query.filter(
        ValeAlmacen.id_tipo_mov_almacen == id_tipo_mov,
        ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt)
    ).all()
    output = [vale.to_dict() for vale in vales]

    return jsonify({'vales_almacen': output}), 200

# Consultar vales por tipo movimiento de documento, numero de documento y fecha inicio y fin
@vale_almacen_bp.route('/vales_almacen/tipo_doc/<int:id_tipo_doc>/nro_doc/<string:nro_doc>/fecha_inicio/<string:fecha_inicio>/fecha_fin/<string:fecha_fin>', methods=['GET'])
@token_required
def ConsultarValesTipoDocNroDocFecha(current_user, id_tipo_doc, nro_doc, fecha_inicio, fecha_fin):
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400

    vales = ValeAlmacen.query.filter(
        ValeAlmacen.id_tipo_doc == id_tipo_doc,      # ✅ Campo correcto
        ValeAlmacen.nro_documento == nro_doc,        # ✅ Campo correcto
        ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt)
    ).all()
    output = [vale.to_dict() for vale in vales]

    return jsonify({'vales_almacen': output}), 200

# Buscar vales por usuario y fecha inicio y fin
@vale_almacen_bp.route('/vales_almacen/usuario/<string:usuario>/fecha_inicio/<string:fecha_inicio>/fecha_fin/<string:fecha_fin>', methods=['GET'])
@token_required
def BuscarValesUsuarioFecha(current_user, usuario, fecha_inicio, fecha_fin):
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400

    # Usar join para buscar por nombre de usuario
    vales = ValeAlmacen.query.join(Usuario).filter(
        Usuario.nombre_user.ilike(f'%{usuario}%'),  # ✅ Campo correcto
        ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt)
    ).all()
    output = [vale.to_dict() for vale in vales]

    return jsonify({'vales_almacen': output}), 200

# Buscar vales por entidad y fecha inicio y fin
@vale_almacen_bp.route('/vales_almacen/entidad/<string:entidad>/fecha_inicio/<string:fecha_inicio>/fecha_fin/<string:fecha_fin>', methods=['GET'])
@token_required
def BuscarValesEntidadFecha(current_user, entidad, fecha_inicio, fecha_fin):
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400

    vales = ValeAlmacen.query.filter(
        ValeAlmacen.entidad.nombre_entidad.ilike(f'%{entidad}%'),
        ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt)
    ).all()
    output = [vale.to_dict() for vale in vales]

    return jsonify({'vales_almacen': output}), 200

# Buscar vales por almacen y fecha inicio y fin
@vale_almacen_bp.route('/vales_almacen/almacen/<string:almacen>/fecha_inicio/<string:fecha_inicio>/fecha_fin/<string:fecha_fin>', methods=['GET'])
@token_required
def BuscarValesAlmacenFecha(current_user, almacen, fecha_inicio, fecha_fin):
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400

    vales = ValeAlmacen.query.filter(
        ValeAlmacen.almacen.nombre_almacen.ilike(f'%{almacen}%'),
        ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt)
    ).all()
    output = [vale.to_dict() for vale in vales]

    return jsonify({'vales_almacen': output}), 200

# Mostrar detalles de un vale de almacén por ID del vale
@vale_almacen_bp.route('/vales_almacen/<int:id_vale>/detalles', methods=['GET'])
@token_required
def MostrarDetallesValeAlmacen(current_user, id_vale):
    vale = ValeAlmacen.query.get(id_vale)
    if not vale:
        return jsonify({"message": "Vale de almacén no encontrado"}), 404

    detalles = [detalle.to_dict() for detalle in vale.detalles]

    return jsonify({'detalles': detalles}), 200

#Consultar vales por rango de fechas
@vale_almacen_bp.route('/vales_almacen/fecha_inicio/<string:fecha_inicio>/fecha_fin/<string:fecha_fin>', methods=['GET'])
@token_required
def ConsultarValesRangoFechas(current_user, fecha_inicio, fecha_fin):
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400

    vales = ValeAlmacen.query.filter(
        ValeAlmacen.fecha_vale.between(fecha_inicio_dt, fecha_fin_dt)
    ).all()
    output = [vale.to_dict() for vale in vales]

    return jsonify({'vales_almacen': output}), 200

# Ingresar vale de almacén
@vale_almacen_bp.route('/vales_almacen', methods=['POST'])
@token_required
def IngresarValeAlmacen(current_user):
    data = request.get_json()

    if not data or 'cod_vale_almacen' not in data or 'id_almacen' not in data or 'id_tipo_mov_almacen' not in data or 'id_user' not in data:
        return jsonify({"message": "Datos incompletos para crear el vale de almacén"}), 400

    # Verificar si el código ya existe
    if ValeAlmacen.query.filter_by(cod_vale_almacen=data['cod_vale_almacen']).first():
        return jsonify({"message": "El código de vale ya existe"}), 400

    nuevo_vale = ValeAlmacen(
        cod_vale_almacen=data['cod_vale_almacen'],
        id_almacen=data['id_almacen'],
        fecha_vale=datetime.strptime(data.get('fecha_vale', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d'),
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

    return jsonify({"message": "Vale de almacén creado exitosamente", "id_vale_almacen": nuevo_vale.id_vale_almacen}), 201

# Ingresar detalles del vale de almacén
@vale_almacen_bp.route('/vales_almacen/<int:id_vale>/detalles', methods=['POST'])
@token_required
def IngresarDetallesValeAlmacen(current_user, id_vale):
    vale = ValeAlmacen.query.get(id_vale)
    if not vale:
        return jsonify({"message": "Vale de almacén no encontrado"}), 404

    data = request.get_json()
    if not data or 'detalles' not in data or not isinstance(data['detalles'], list):
        return jsonify({"message": "Datos incompletos para agregar detalles"}), 400

    for detalle_data in data['detalles']:
        if 'id_articulo' not in detalle_data or 'cantidad' not in detalle_data or 'precio_soles' not in detalle_data:
            return jsonify({"message": "Datos incompletos en uno de los detalles"}), 400

        nuevo_detalle = ValeAlmacenDet(
            id_vale_almacen=id_vale,
            id_articulo=detalle_data['id_articulo'],        # ✅ Campo correcto
            cantidad=detalle_data['cantidad'],
            precio_soles=detalle_data['precio_soles'],      # ✅ Campo correcto
            item=detalle_data.get('item')  # Opcional, si se envía
        )
        db.session.add(nuevo_detalle)

    db.session.commit()

    return jsonify({"message": "Detalles agregados exitosamente al vale de almacén"}), 201

# Modificar vale de almacen
@vale_almacen_bp.route('/vales_almacen/<int:id_vale>', methods=['PUT'])
@token_required
def ModificarValeAlmacen(current_user, id_vale):
    vale = ValeAlmacen.query.get(id_vale)
    if not vale:
        return jsonify({"message": "Vale de almacén no encontrado"}), 404

    data = request.get_json()
    vale.cod_vale_almacen = data.get('cod_vale_almacen', vale.cod_vale_almacen)
    vale.id_almacen = data.get('id_almacen', vale.id_almacen)
    if 'fecha_vale' in data:
        try:
            vale.fecha_vale = datetime.strptime(data['fecha_vale'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Formato de fecha inválido. Use YYYY-MM-DD."}), 400
    vale.id_tipo_mov_almacen = data.get('id_tipo_mov_almacen', vale.id_tipo_mov_almacen)
    vale.id_user = data.get('id_user', vale.id_user)
    vale.id_entidad = data.get('id_entidad', vale.id_entidad)
    vale.id_tipo_doc = data.get('id_tipo_doc', vale.id_tipo_doc)
    vale.serie_doc = data.get('serie_doc', vale.serie_doc)
    vale.nro_documento = data.get('nro_documento', vale.nro_documento)
    vale.flag_estado = data.get('flag_estado', vale.flag_estado)

    db.session.commit()

    return jsonify({"message": "Vale de almacén modificado exitosamente"}), 200

# Inactivar vale de almacen y su detalles
@vale_almacen_bp.route('/vales_almacen/<int:id_vale>', methods=['DELETE'])
@token_required
def InactivarValeAlmacen(current_user, id_vale):
    vale = ValeAlmacen.query.get(id_vale)
    if not vale:
        return jsonify({"message": "Vale de almacén no encontrado"}), 404

    vale.flag_estado = '0'
    for detalle in vale.detalles:
        detalle.flag_estado = '0'

    db.session.commit()

    return jsonify({"message": "Vale de almacén y sus detalles inactivados exitosamente"}), 200