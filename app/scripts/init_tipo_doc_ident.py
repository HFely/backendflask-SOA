# app/scripts/init_tipo_doc_ident.py
from app.extensions import db
from app.models.tipo_doc_ident import TipoDocIdent

def init_tipo_doc_ident():
    """Inicializa los tipos de documento de identidad por defecto"""
    tipos_doc = [
        {'id': 1, 'nombre': 'DNI'},
        {'id': 2, 'nombre': 'RUC'},
        {'id': 3, 'nombre': 'Carnet de Extranjería'},
        {'id': 4, 'nombre': 'Pasaporte'},
        {'id': 5, 'nombre': 'Otros'}  # Para otros tipos de documentos no especificados}
    ]
    
    created_count = 0
    for tipo in tipos_doc:
        existing = TipoDocIdent.query.get(tipo['id'])
        if not existing:
            nuevo_tipo = TipoDocIdent(
                id_tipo_doc_ident=tipo['id'],
                nombre_tipo_doc_ident=tipo['nombre'],
                flag_estado='1'
            )
            db.session.add(nuevo_tipo)
            created_count += 1
        else:
            # Actualizar si ya existe pero está inactivo
            if existing.flag_estado != '1':
                existing.flag_estado = '1'
                existing.nombre_tipo_doc_ident = tipo['nombre']
                created_count += 1
    
    db.session.commit()
    return created_count