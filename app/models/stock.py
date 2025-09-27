# app/models/stock.py
from app.extensions import db

#Tabla que se actualiza por trigger de los movimientos de almacén.
class Stock(db.Model):
    __tablename__ = 'stock'
    
    id_almacen = db.Column(db.Integer, db.ForeignKey('almacen.id_almacen'), primary_key=True)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id_articulo'), primary_key=True)
    cantidad = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    precio_promedio = db.Column(db.Numeric(16, 4), nullable=False, default=0)
    
    # Relaciones
    almacen = db.relationship('Almacen', backref='stocks')
    articulo = db.relationship('Articulo', backref='stocks')
    
    def __repr__(self):
        return f'<Stock {self.id_almacen}-{self.id_articulo}>'