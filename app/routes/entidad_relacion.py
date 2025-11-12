# app/routes/entidad_relacion.py
from flask import Blueprint, request, jsonify
from app.models.entidad_relacion import EntidadRelacion
from app.extensions import db
from app.services.auth_service import generate_token
from app.decorators.PyJWT import token_required

entidad_relacion_bp = Blueprint('entidad_relacion', __name__)

# Obtener todas las entidades_relaciones
@entidad_relacion_bp.route('/', methods=['GET'])
@token_required
def ConsultarEntidadesRelaciones(current_user):
    entidades = EntidadRelacion.query.all()
    output = [entidad.to_dict() for entidad in entidades]

    return jsonify({'entidades_relaciones': output}), 200

# Obtener una entidad_relacion por ID
@entidad_relacion_bp.route('/<int:id_entidad>', methods=['GET'])
@token_required
def ConsultarEntidadRelacionID(current_user, id_entidad):
    entidad = EntidadRelacion.query.get(id_entidad)
    if not entidad:
        return jsonify({"message": "Entidad de relación no encontrada"}), 404

    return jsonify(entidad.to_dict()), 200

# Consultar entidades_relaciones por tipo de documento de identidad
@entidad_relacion_bp.route('/tipo_doc/<int:id_tipo_doc>', methods=['GET'])
@token_required
def ConsultarEntidadesRelacionesTipoDoc(current_user, id_tipo_doc):
    entidades = EntidadRelacion.query.filter_by(id_tipo_doc_ident=id_tipo_doc).all()
    output = [entidad.to_dict() for entidad in entidades]

    return jsonify({'entidades_relaciones': output}), 200

#Consultar entidades_relaciones por numero de documento de identidad y tipo de documento de identidad
@entidad_relacion_bp.route('/doc/<string:nro_doc_ident>/tipo_doc/<int:id_tipo_doc>', methods=['GET'])
@token_required
def ConsultarEntidadesRelacionesNroDocTipoDoc(current_user, nro_doc_ident, id_tipo_doc):
    entidades = EntidadRelacion.query.filter_by(nro_doc_ident=nro_doc_ident, id_tipo_doc_ident=id_tipo_doc).all()
    output = [entidad.to_dict() for entidad in entidades]

    return jsonify({'entidades_relaciones': output}), 200

#Buscar entidades_relaciones por nombre (búsqueda parcial)
@entidad_relacion_bp.route('/buscar/<string:nombre>', methods=['GET'])
@token_required
def BuscarEntidadesRelacionesNombre(current_user, nombre):
    entidades = EntidadRelacion.query.filter(EntidadRelacion.nombre_entidad.ilike(f'%{nombre}%')).all()
    output = [entidad.to_dict() for entidad in entidades]

    return jsonify({'entidades_relaciones': output}), 200

#Filtrar entidades_relaciones por proveedores
@entidad_relacion_bp.route('/proveedores', methods=['GET'])
@token_required
def FiltrarEntidadesRelacionesProveedores(current_user):
    entidades = EntidadRelacion.query.filter_by(flag_proveedor='1').all()
    output = [entidad.to_dict() for entidad in entidades]

    return jsonify({'entidades_relaciones': output}), 200

#Filtrar entidades_relaciones por clientes
@entidad_relacion_bp.route('/clientes', methods=['GET'])
@token_required
def FiltrarEntidadesRelacionesClientes(current_user):
    entidades = EntidadRelacion.query.filter_by(flag_cliente='1').all()
    output = [entidad.to_dict() for entidad in entidades]

    return jsonify({'entidades_relaciones': output}), 200

# Crear una nueva entidad_relacion (solo para administradores)
@entidad_relacion_bp.route('/', methods=['POST'])
@token_required
def CrearEntidadRelacion(current_user):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    data = request.get_json()
    nombre_entidad = data.get("nombre_entidad")
    id_tipo_doc_ident = data.get("id_tipo_doc_ident")
    nro_doc_ident = data.get("nro_doc_ident")
    
    # Campos opcionales
    direccion = data.get("direccion", "")
    telefono = data.get("telefono", "")
    flag_proveedor = data.get("flag_proveedor", '0')
    flag_cliente = data.get("flag_cliente", '0')
    flag_estado = data.get("flag_estado", '1')

    # Validaciones
    if not all([nombre_entidad, id_tipo_doc_ident, nro_doc_ident]):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    # Validar que no exista el mismo nombre
    if EntidadRelacion.query.filter_by(nombre_entidad=data['nombre_entidad']).first():
        return jsonify({"message": "El nombre de la entidad ya existe"}), 400

    # Validar que no exista el mismo documento identidad con el mismo tipo
    if EntidadRelacion.query.filter_by(
        nro_doc_ident=data['nro_doc_ident'],
        id_tipo_doc_ident=data['id_tipo_doc_ident']
    ).first():
        return jsonify({"message": "Ya existe una entidad con este documento de identidad"}), 400

    if EntidadRelacion.query.filter_by(nombre_entidad=nombre_entidad).first():
        return jsonify({"message": "El nombre de la entidad ya existe"}), 400

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

    return jsonify({"message": "Entidad de relación creada exitosamente"}), 201

# Actualizar una entidad_relacion (solo para administradores)
@entidad_relacion_bp.route('/<int:id_entidad>', methods=['PUT'])
@token_required
def ActualizarEntidadRelacion(current_user, id_entidad):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    entidad = EntidadRelacion.query.get(id_entidad)
    if not entidad:
        return jsonify({"message": "Entidad de relación no encontrada"}), 404

    data = request.get_json()
    
    # Validar unicidad del nombre si se está cambiando
    if 'nombre_entidad' in data and data['nombre_entidad'] != entidad.nombre_entidad:
        if EntidadRelacion.query.filter_by(nombre_entidad=data['nombre_entidad']).first():
            return jsonify({"message": "El nombre de la entidad ya existe"}), 400

    # Validar unicidad del documento si se está cambiando
    if ('nro_doc_ident' in data and data['nro_doc_ident'] != entidad.nro_doc_ident) or \
       ('id_tipo_doc_ident' in data and data['id_tipo_doc_ident'] != entidad.id_tipo_doc_ident):
        
        nro_doc = data.get('nro_doc_ident', entidad.nro_doc_ident)
        tipo_doc = data.get('id_tipo_doc_ident', entidad.id_tipo_doc_ident)
        
        existing = EntidadRelacion.query.filter(
            EntidadRelacion.nro_doc_ident == nro_doc,
            EntidadRelacion.id_tipo_doc_ident == tipo_doc,
            EntidadRelacion.id_entidad != id_entidad  # Excluir la entidad actual
        ).first()
        
        if existing:
            return jsonify({"message": "Ya existe otra entidad con este documento de identidad"}), 400

    # Actualizar campos
    campos = ['nombre_entidad', 'id_tipo_doc_ident', 'nro_doc_ident', 'direccion', 
              'telefono', 'flag_proveedor', 'flag_cliente', 'flag_estado']
    
    for campo in campos:
        if campo in data:
            setattr(entidad, campo, data[campo])

    db.session.commit()

    return jsonify({"message": "Entidad de relación actualizada exitosamente"}), 200

# Inactivar una entidad_relacion (solo para administradores)
@entidad_relacion_bp.route('/<int:id_entidad>', methods=['DELETE'])
@token_required
def InactivarEntidadRelacion(current_user, id_entidad):
    if current_user.flag_administrador != '1':
        return jsonify({"message": "Acceso denegado"}), 403

    entidad = EntidadRelacion.query.get(id_entidad)
    if not entidad:
        return jsonify({"message": "Entidad de relación no encontrada"}), 404

    entidad.flag_estado = '0'
    db.session.commit()

    return jsonify({"message": "Entidad de relación inactivada exitosamente"}), 200

# Reactivar una entidad_relacion (solo para administradores)
# @entidad_relacion_bp.route('/entidades_relaciones/<int:id_entidad>/reactivar', methods=['PUT'])
# @token_required
# def ReactivarEntidadRelacion(current_user, id_entidad):
#     if current_user.flag_administrador != '1':
#         return jsonify({"message": "Acceso denegado"}), 403

#     entidad = EntidadRelacion.query.get(id_entidad)
#     if not entidad:
#         return jsonify({"message": "Entidad de relación no encontrada"}), 404

#     entidad.flag_estado = '1'
#     db.session.commit()

#     return jsonify({"message": "Entidad de relación reactivada exitosamente"}), 200