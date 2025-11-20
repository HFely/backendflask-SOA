# app/scripts/init_categorias.py
from app.extensions import db
from app.models.categoria import Categoria

def init_categorias():
    """Inicializa categorías específicas para cadena de venta al por mayor (Makro)"""
    
    categorias_makro = [
        # ========== ALIMENTOS Y BEBIDAS ==========
        {'id': 1, 'codigo': 'ABAR', 'nombre': 'ABARROTES'},
        {'id': 2, 'codigo': 'LACTE', 'nombre': 'LÁCTEOS Y HUEVOS'},
        {'id': 3, 'codigo': 'CARNES', 'nombre': 'CARNES Y AVES'},
        {'id': 4, 'codigo': 'PESCA', 'nombre': 'PESCADOS Y MARISCOS'},
        {'id': 5, 'codigo': 'FRUTV', 'nombre': 'FRUTAS Y VERDURAS'},
        {'id': 6, 'codigo': 'PANAD', 'nombre': 'PANADERÍA Y REPOSTERÍA'},
        {'id': 7, 'codigo': 'CONGE', 'nombre': 'PRODUCTOS CONGELADOS'},
        {'id': 8, 'codigo': 'BEBID', 'nombre': 'BEBIDAS Y LICORES'},
        
        # ========== PRODUCTOS NO ALIMENTARIOS ==========
        {'id': 9, 'codigo': 'LIMPIE', 'nombre': 'PRODUCTOS DE LIMPIEZA'},
        {'id': 10, 'codigo': 'HIGIEN', 'nombre': 'HIGIENE PERSONAL'},
        {'id': 11, 'codigo': 'PAPEL', 'nombre': 'PAPELERÍA Y OFICINA'},
        {'id': 12, 'codigo': 'ELECTR', 'nombre': 'ELECTRODOMÉSTICOS'},
        {'id': 13, 'codigo': 'HOGAR', 'nombre': 'ARTÍCULOS PARA EL HOGAR'},
        {'id': 14, 'codigo': 'TEXTIL', 'nombre': 'TEXTILES Y ROPA'},
        
        # ========== PARA PROFESIONALES (HORECA) ==========
        {'id': 15, 'codigo': 'HORECA', 'nombre': 'EQUIPOS HORECA'},
        {'id': 16, 'codigo': 'COCINA', 'nombre': 'UTENSILIOS COCINA'},
        {'id': 17, 'codigo': 'VAILLA', 'nombre': 'VAJILLA Y CRISTALERÍA'},
        {'id': 18, 'codigo': 'MOBILI', 'nombre': 'MOBILIARIO RESTAURANTE'},
        {'id': 19, 'codigo': 'UNIFOR', 'nombre': 'UNIFORMES Y LENCERÍA'},
        
        # ========== CATEGORÍAS OPERATIVAS ==========
        {'id': 20, 'codigo': 'MATEMP', 'nombre': 'MATERIALES EMPAQUE'},
        {'id': 21, 'codigo': 'SEGURI', 'nombre': 'SEGURIDAD INDUSTRIAL'},
        {'id': 22, 'codigo': 'MANTEN', 'nombre': 'MANTENIMIENTO'},
        {'id': 23, 'codigo': 'PERECE', 'nombre': 'PRODUCTOS PERECIBLES'},
        {'id': 24, 'codigo': 'NOPERE', 'nombre': 'NO PERECIBLES'}
    ]
    
    created_count = 0
    for cat in categorias_makro:
        existing = Categoria.query.get(cat['id'])
        if not existing:
            nueva_categoria = Categoria(
                id_categoria=cat['id'],
                cod_categoria=cat['codigo'],
                nombre_categoria=cat['nombre'],
                flag_estado='1'
            )
            db.session.add(nueva_categoria)
            created_count += 1
        else:
            # Actualizar si existe pero con datos diferentes
            if (existing.nombre_categoria != cat['nombre'] or 
                existing.cod_categoria != cat['codigo'] or
                existing.flag_estado != '1'):
                
                existing.nombre_categoria = cat['nombre']
                existing.cod_categoria = cat['codigo']
                existing.flag_estado = '1'
                created_count += 1
    
    db.session.commit()
    return created_count

def get_categorias_activas():
    """Obtener lista de categorías activas"""
    return Categoria.query.filter_by(flag_estado='1').order_by(Categoria.cod_categoria).all()