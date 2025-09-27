# app/models/tipo_mov_almacen.py
from app.extensions import db

# Tabla donde se registran los tipos de movimientos que se usan en los vales de almacén. (Ejemplo: Ingreso por compra, Ingreso por devolución, Salida por venta, Salida por consumo interno, etc.)
class TipoMovAlmacen(db.Model):
    __tablename__ = 'tipo_mov_almacen'
    
    id_tipo_mov_almacen = db.Column(db.Integer, primary_key=True)
    cod_tipo_mov_alm = db.Column(db.String(3), unique=True, nullable=False)
    desc_tipo_mov_almacen = db.Column(db.String(90), nullable=False) #Descripción del tipo de movimiento de almacén
    factor_mov = db.Column(db.Numeric(1, 0), nullable=False)  # 1=Ingreso, -1=Salida
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    def __repr__(self):
        return f'<TipoMovAlmacen {self.cod_tipo_mov_alm}>'