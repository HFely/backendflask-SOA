# app/models/unidad.py
from app.extensions import db

# Tabla donde se registran las unidades de medida (Ejemplo: KG, LITRO, UNIDAD, CAJA, etc.)
class Unidad(db.Model):
    __tablename__ = 'unidad'
    
    cod_unidad = db.Column(db.String(4), primary_key=True)
    nombre_unidad = db.Column(db.String(30), nullable=False)
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    def __repr__(self):
        return f'<Unidad {self.cod_unidad}>'