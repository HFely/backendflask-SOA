# app/utils/data_checker.py
from app.models.tipo_doc_ident import TipoDocIdent

def ensure_essential_data():
    """Verificar que existan datos esenciales al iniciar la aplicación"""
    
    # Verificar si existen tipos de documento
    if TipoDocIdent.query.count() == 0:
        print("Advertencia: No hay tipos de documento configurados")
        print("Ejecuta: flask init-data")
        return False
    
    # Verificar que exista al menos el DNI (id=1)
    dni = TipoDocIdent.query.get(1)
    if not dni or dni.flag_estado != '1':
        print("Advertencia: El DNI (id=1) no está configurado")
        print("Ejecuta: flask init-data")
        return False
    
    return True