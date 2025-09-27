from app.extensions import db
from app.models.unidad import Unidad

def init_unidades():
    unidades = [
        {'codigo': 'UNI', 'nombre': 'UNIDAD'},
        {'codigo': 'KG', 'nombre': 'KILOGRAMO'},
        {'codigo': 'GR', 'nombre': 'GRAMO'},
        {'codigo': 'LT', 'nombre': 'LITRO'},
        {'codigo': 'ML', 'nombre': 'MILILITRO'},
        {'codigo': 'MTS', 'nombre': 'METROS'},
        {'codigo': 'CM', 'nombre': 'CENTIMETROS'},
        {'codigo': 'CJA', 'nombre': 'CAJA'},
        {'codigo': 'PQT', 'nombre': 'PAQUETE'}
    ]
    
    for unidad in unidades:
        if not Unidad.query.get(unidad['codigo']):
            nueva_unidad = Unidad(
                cod_unidad=unidad['codigo'],
                nombre_unidad=unidad['nombre'],
                flag_estado='1'
            )
            db.session.add(nueva_unidad)
    
    db.session.commit()