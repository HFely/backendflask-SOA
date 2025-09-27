# app/models/kardex.py
from app.extensions import db
from datetime import datetime

# Tabla para apoyo de reportes de movimientos de almacén (Kardex)
class Kardex(db.Model):
    __tablename__ = 'kardex'
    
    id_kardex = db.Column(db.Integer, primary_key=True)
    id_almacen = db.Column(db.Integer, db.ForeignKey('almacen.id_almacen'), nullable=False)
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id_articulo'), nullable=False)
    id_vale_almacen_det = db.Column(db.Integer, db.ForeignKey('vale_almacen_det.id_vale_almacen_det'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cantidad = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    precio_soles = db.Column(db.Numeric(16, 4), nullable=False, default=0)
    
    # Relaciones
    almacen = db.relationship('Almacen', backref='kardex')
    articulo = db.relationship('Articulo', backref='kardex')
    vale_detalle = db.relationship('ValeAlmacenDet', backref='kardex')
    
    def __repr__(self):
        return f'<Kardex {self.id_kardex}>'