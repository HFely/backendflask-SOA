# app/scripts/init_data.py
from .init_tipo_doc_ident import init_tipo_doc_ident
from .init_unidades import init_unidades
from .init_categorias import init_categorias
from .init_tipos_movimiento import init_tipos_movimiento
from .init_almacenes import init_almacenes
from .init_tipos_documento import init_tipos_documento

def init_data():
    """Inicializar todos los datos por defecto"""
    print("Inicializando datos esenciales...")
    
    result_tipos_doc = init_tipo_doc_ident()
    result_unidades = init_unidades()
    result_categorias = init_categorias()
    result_movimientos = init_tipos_movimiento()  # ← Nuevo script
    result_almacenes = init_almacenes()
    result_tipos_doc = init_tipos_documento()
    
    print(f"✓ Tipos documento: {result_tipos_doc} registros")
    print(f"✓ Unidades: {result_unidades} registros")
    print(f"✓ Categorías: {result_categorias} registros")
    print(f"✓ Tipos movimiento: {result_movimientos} registros")
    print(f"✓ Almacenes: {result_almacenes} registros")
    print(f"✓ Tipos documento: {result_tipos_doc} registros")
    
    print("Todos los datos inicializados correctamente")
