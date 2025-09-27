# app/scripts/init_almacenes.py
from app.extensions import db
from app.models.almacen import Almacen

def init_almacenes():
    """Inicializa los almacenes con nombres comerciales realistas"""
    
    almacenes = [
        # G = General, M = Materiales, P = Materia Prima, T = Productos Terminados, O = Otros
        {'id': 1, 'codigo': 'ALM001', 'nombre': 'ALMACÉN PRINCIPAL - MERCANCÍA VENTA', 'tipo': 'G'},
        {'id': 2, 'codigo': 'ALM002', 'nombre': 'ALMACÉN MATERIA PRIMA', 'tipo': 'P'},
        {'id': 3, 'codigo': 'ALM003', 'nombre': 'ALMACÉN PRODUCTOS TERMINADOS', 'tipo': 'T'},
        {'id': 4, 'codigo': 'ALM004', 'nombre': 'ALMACÉN ACTIVOS FIJOS', 'tipo': 'O'},
        {'id': 5, 'codigo': 'ALM005', 'nombre': 'ALMACÉN HERRAMIENTAS Y EQUIPOS', 'tipo': 'M'},
        {'id': 6, 'codigo': 'ALM006', 'nombre': 'ALMACÉN MATERIALES DE OFICINA', 'tipo': 'M'},
        {'id': 7, 'codigo': 'ALM007', 'nombre': 'ALMACÉN PRODUCTOS PERECIBLES', 'tipo': 'T'},
        {'id': 8, 'codigo': 'ALM008', 'nombre': 'ALMACÉN DEVOLUCIONES Y MERMAS', 'tipo': 'O'},
        {'id': 9, 'codigo': 'ALM009', 'nombre': 'ALMACÉN MATERIALES EN CONSIGNACIÓN', 'tipo': 'O'},
        {'id': 10, 'codigo': 'ALM010', 'nombre': 'ALMACÉN PRODUCTOS EN CUARENTENA', 'tipo': 'O'}
    ]
    
    created_count = 0
    for alm in almacenes:
        # Verificar si ya existe por ID o por código
        existing_by_id = Almacen.query.get(alm['id'])
        existing_by_code = Almacen.query.filter_by(cod_almacen=alm['codigo']).first()
        
        if not existing_by_id and not existing_by_code:
            nuevo_almacen = Almacen(
                id_almacen=alm['id'],
                cod_almacen=alm['codigo'],
                nombre_almacen=alm['nombre'],
                flag_tipo_almacen=alm['tipo'],
                flag_estado='1'
            )
            db.session.add(nuevo_almacen)
            created_count += 1
        elif existing_by_id:
            # Actualizar si existe pero con datos diferentes
            if (existing_by_id.nombre_almacen != alm['nombre'] or 
                existing_by_id.flag_tipo_almacen != alm['tipo'] or
                existing_by_id.flag_estado != '1'):
                
                existing_by_id.nombre_almacen = alm['nombre']
                existing_by_id.flag_tipo_almacen = alm['tipo']
                existing_by_id.flag_estado = '1'
                created_count += 1
    
    db.session.commit()
    return created_count

def get_almacenes_activos():
    """Obtener lista de almacenes activos"""
    return Almacen.query.filter_by(flag_estado='1').order_by(Almacen.cod_almacen).all()