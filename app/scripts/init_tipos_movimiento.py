# app/scripts/init_tipos_movimiento.py
from app.extensions import db
from app.models.tipo_mov_almacen import TipoMovAlmacen

def init_tipos_movimiento():
    """Inicializa los tipos de movimiento de almacén principales"""
    
    movimientos_principales = [
        # ========== INGRESOS (factor = 1) ==========
        {'id': 1, 'codigo': 'I00', 'nombre': 'INVENTARIO INICIAL', 'factor': 1},
        {'id': 2, 'codigo': 'I01', 'nombre': 'INGRESO POR COMPRA', 'factor': 1},
        {'id': 3, 'codigo': 'I03', 'nombre': 'INGRESO POR TRANSFERENCIA', 'factor': 1},
        {'id': 4, 'codigo': 'I04', 'nombre': 'INGRESO POR DEVOLUCION PROVEEDOR', 'factor': 1},
        {'id': 5, 'codigo': 'I05', 'nombre': 'INGRESO POR CONSIGNACION', 'factor': 1},
        {'id': 6, 'codigo': 'I08', 'nombre': 'INGRESO POR AJUSTE INVENTARIO', 'factor': 1},
        {'id': 7, 'codigo': 'I09', 'nombre': 'INGRESO POR PRODUCCION', 'factor': 1},
        {'id': 8, 'codigo': 'I14', 'nombre': 'INGRESO POR DEVOLUCION ALMACEN', 'factor': 1},
        {'id': 9, 'codigo': 'I30', 'nombre': 'INGRESO POR DONACION', 'factor': 1},
        {'id': 10, 'codigo': 'I39', 'nombre': 'INGRESO POR DEVOLUCION VENTA', 'factor': 1},
        
        # ========== SALIDAS (factor = -1) ==========
        {'id': 11, 'codigo': 'S01', 'nombre': 'SALIDA POR CONSUMOS INTERNOS', 'factor': -1},
        {'id': 12, 'codigo': 'S02', 'nombre': 'SALIDA POR VENTA PRODUCTOS', 'factor': -1},
        {'id': 13, 'codigo': 'S03', 'nombre': 'SALIDA POR TRANSFERENCIA', 'factor': -1},
        {'id': 14, 'codigo': 'S04', 'nombre': 'SALIDA POR DEVOLUCION PROVEEDOR', 'factor': -1},
        {'id': 15, 'codigo': 'S08', 'nombre': 'SALIDA POR AJUSTE INVENTARIO', 'factor': -1},
        {'id': 16, 'codigo': 'S14', 'nombre': 'SALIDA POR BAJA INVENTARIO', 'factor': -1},
        {'id': 17, 'codigo': 'S16', 'nombre': 'SALIDA POR VENTA MATERIALES', 'factor': -1},
        {'id': 18, 'codigo': 'S20', 'nombre': 'SALIDA POR OBSEQUIO', 'factor': -1},
        {'id': 19, 'codigo': 'S21', 'nombre': 'SALIDA POR DONACION', 'factor': -1},
        {'id': 20, 'codigo': 'S35', 'nombre': 'SALIDA POR SUSTRACCION (ROBO)', 'factor': -1},
        {'id': 21, 'codigo': 'S40', 'nombre': 'SALIDA POR CONSUMO MUESTRA', 'factor': -1}
    ]
    
    created_count = 0
    for mov in movimientos_principales:
        # Verificar si ya existe por código
        existing = TipoMovAlmacen.query.filter_by(cod_tipo_mov_alm=mov['codigo']).first()
        
        if not existing:
            nuevo_mov = TipoMovAlmacen(
                id_tipo_mov_almacen=mov['id'],
                cod_tipo_mov_alm=mov['codigo'],
                desc_tipo_mov_almacen=mov['nombre'],
                factor_mov=mov['factor'],
                flag_estado='1'
            )
            db.session.add(nuevo_mov)
            created_count += 1
        else:
            # Actualizar si existe pero está inactivo o con datos diferentes
            if (existing.flag_estado != '1' or 
                existing.desc_tipo_mov_almacen != mov['nombre'] or 
                existing.factor_mov != mov['factor']):
                
                existing.desc_tipo_mov_almacen = mov['nombre']
                existing.factor_mov = mov['factor']
                existing.flag_estado = '1'
                created_count += 1
    
    db.session.commit()
    return created_count

def get_tipos_movimiento_activos():
    """Obtener lista de tipos de movimiento activos"""
    return TipoMovAlmacen.query.filter_by(flag_estado='1').order_by(
        TipoMovAlmacen.factor_mov.desc(), 
        TipoMovAlmacen.cod_tipo_mov_alm
    ).all()