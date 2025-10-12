# app/models/vale_almacen_det.py
from app.extensions import db

# Tabla donde se registra el detalle de un vale de almacén
class ValeAlmacenDet(db.Model):
    __tablename__ = 'vale_almacen_det'
    
    id_vale_almacen_det = db.Column(db.Integer, primary_key=True)
    id_vale_almacen = db.Column(db.Integer, db.ForeignKey('vale_almacen.id_vale_almacen'), nullable=False)
    item = db.Column(db.Numeric(4, 0))
    id_articulo = db.Column(db.Integer, db.ForeignKey('articulo.id_articulo'), nullable=False)
    cantidad = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    precio_soles = db.Column(db.Numeric(12, 4), nullable=False, default=0)
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    # Relaciones
    articulo = db.relationship('Articulo', backref='detalles_vales')
    
    def __repr__(self):
        return f'<ValeAlmacenDet {self.id_vale_almacen_det}>'
    
    def to_dict(self):
        return {
            'id_vale_almacen_det': self.id_vale_almacen_det,
            'id_vale_almacen': self.id_vale_almacen,
            'item': float(self.item) if self.item else None,
            'id_articulo': self.id_articulo,
            'cantidad': float(self.cantidad) if self.cantidad else 0,
            'precio_soles': float(self.precio_soles) if self.precio_soles else 0,
            'flag_estado': self.flag_estado,
            'articulo_nombre': self.articulo.nombre_articulo if self.articulo else None
        }