# app/models/almacen.py
from app.extensions import db

# Tabla donde se registran los almacenes (Ejemplo: Almacén General, Almacén de Materia Prima, Almacén de Productos Terminados, etc.)
class Almacen(db.Model):
    __tablename__ = 'almacen'
    
    id_almacen = db.Column(db.Integer, primary_key=True)
    cod_almacen = db.Column(db.String(6), unique=True, nullable=False)
    nombre_almacen = db.Column(db.String(50), nullable=False)
    flag_tipo_almacen = db.Column(db.String(1), nullable=False)  # G,M,P,T,O
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    def __repr__(self):
        return f'<Almacen {self.cod_almacen}>'