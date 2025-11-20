# app/scripts/init_tipos_documento.py
from app.extensions import db
from app.models.tipo_documento import TipoDocumento

def init_tipos_documento():
    """Inicializa tipos de documento para gestión de inventario mayorista"""
    
    tipos_documento = [
        # ========== DOCUMENTOS LEGALES (SUNAT) ==========
        {'id': 1, 'codigo': 'FACT', 'nombre': 'FACTURA'},
        {'id': 2, 'codigo': 'BOL', 'nombre': 'BOLETA DE VENTA'},
        {'id': 3, 'codigo': 'GR', 'nombre': 'GUÍA DE REMISIÓN'},
        {'id': 4, 'codigo': 'NC', 'nombre': 'NOTA DE CRÉDITO'},
        {'id': 5, 'codigo': 'ND', 'nombre': 'NOTA DE DÉBITO'},
        {'id': 6, 'codigo': 'FE', 'nombre': 'FACTURA ELECTRÓNICA'},
        
        # ========== DOCUMENTOS DE COMPRAS ==========
        {'id': 7, 'codigo': 'OC', 'nombre': 'ORDEN DE COMPRA'},
        {'id': 8, 'codigo': 'COTIZ', 'nombre': 'COTIZACIÓN'},
        {'id': 9, 'codigo': 'REQ', 'nombre': 'REQUERIMIENTO'},
        {'id': 10, 'codigo': 'SOLCOM', 'nombre': 'SOLICITUD DE COMPRA'},
        
        # ========== DOCUMENTOS DE ALMACÉN ==========
        {'id': 11, 'codigo': 'INGALM', 'nombre': 'INGRESO A ALMACÉN'},
        {'id': 12, 'codigo': 'SALALM', 'nombre': 'SALIDA DE ALMACÉN'},
        {'id': 13, 'codigo': 'TRASL', 'nombre': 'TRASLADO INTERNO'},
        {'id': 14, 'codigo': 'AJUSTE', 'nombre': 'AJUSTE DE INVENTARIO'},
        {'id': 15, 'codigo': 'INVINI', 'nombre': 'INVENTARIO INICIAL'},
        {'id': 16, 'codigo': 'INVFIS', 'nombre': 'INVENTARIO FÍSICO'},
        
        # ========== DOCUMENTOS DE VENTAS ==========
        {'id': 17, 'codigo': 'PV', 'nombre': 'PEDIDO DE VENTA'},
        {'id': 18, 'codigo': 'COTV', 'nombre': 'COTIZACIÓN DE VENTA'},
        {'id': 19, 'codigo': 'PREVEN', 'nombre': 'PREVENTA'},
        {'id': 20, 'codigo': 'REMIS', 'nombre': 'REMISIÓN'},
        
        # ========== DOCUMENTOS DE CONTROL ==========
        {'id': 21, 'codigo': 'DEVOL', 'nombre': 'DEVOLUCIÓN'},
        {'id': 22, 'codigo': 'RECEP', 'nombre': 'RECEPCIÓN'},
        {'id': 23, 'codigo': 'CONSIG', 'nombre': 'CONSIGNACIÓN'},
        {'id': 24, 'codigo': 'BAJA', 'nombre': 'BAJA DE INVENTARIO'}
    ]
    
    created_count = 0
    for doc in tipos_documento:
        existing = TipoDocumento.query.get(doc['id'])
        if not existing:
            nuevo_doc = TipoDocumento(
                id_tipo_documento=doc['id'],
                cod_tipo_documento=doc['codigo'],
                nombre_tipo_documento=doc['nombre'],
                flag_estado='1'
            )
            db.session.add(nuevo_doc)
            created_count += 1
        else:
            # Actualizar si existe pero con datos diferentes
            if (existing.nombre_tipo_documento != doc['nombre'] or 
                existing.cod_tipo_documento != doc['codigo'] or
                existing.flag_estado != '1'):
                
                existing.nombre_tipo_documento = doc['nombre']
                existing.cod_tipo_documento = doc['codigo']
                existing.flag_estado = '1'
                created_count += 1
    
    db.session.commit()
    return created_count

def get_tipos_documento_activos():
    """Obtener lista de tipos de documento activos"""
    return TipoDocumento.query.filter_by(flag_estado='1').order_by(TipoDocumento.cod_tipo_documento).all()