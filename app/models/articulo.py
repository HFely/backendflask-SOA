# app/models/articulo.py
from app.extensions import db

# Tabla donde se registran los artículos o productos del inventario (Ejemplo: Laptop, Mesa, Camisa, etc.)
class Articulo(db.Model):
    __tablename__ = 'articulo'
    
    id_articulo = db.Column(db.Integer, primary_key=True)
    cod_articulo = db.Column(db.String(12), unique=True, nullable=False)
    nombre_articulo = db.Column(db.String(200), nullable=False)
    cod_unidad = db.Column(db.String(4), db.ForeignKey('unidad.cod_unidad'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    # Relaciones
    unidad = db.relationship('Unidad', backref='articulos')
    categoria = db.relationship('Categoria', backref='articulos')
    
    def __repr__(self):
        return f'<Articulo {self.cod_articulo}>'