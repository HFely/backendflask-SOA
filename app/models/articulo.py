# app/models/articulo.py
from app.extensions import db

# Tabla donde se registran los artículos o productos del inventario (Ejemplo: Laptop, Mesa, Camisa, etc.)
class Articulo(db.Model):
    __tablename__ = 'articulo'
    
    id_articulo = db.Column(db.Integer, primary_key=True)
    cod_articulo = db.Column(db.String(12), unique=True, nullable=False)
    nombre_articulo = db.Column(db.String(200), nullable=False)
    descripcion_articulo = db.Column(db.String(500))
    precio_articulo = db.Column(db.Float, nullable=False)
    stock_articulo = db.Column(db.Integer, default=0)
    cod_unidad = db.Column(db.String(4), db.ForeignKey('unidad.cod_unidad'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    # Relaciones
    unidad = db.relationship('Unidad', backref='articulos')
    categoria = db.relationship('Categoria', backref='articulos')
    
    def __repr__(self):
        return f'<Articulo {self.cod_articulo}>'
    
    def to_dict(self):
        return {
            'id_articulo': self.id_articulo,
            'cod_articulo': self.cod_articulo,
            'nombre_articulo': self.nombre_articulo,
            'descripcion_articulo': self.descripcion_articulo,
            'precio_articulo': float(self.precio_articulo),  # Convertir Decimal a float para JSON
            'stock_articulo': self.stock_articulo,
            'cod_unidad': self.cod_unidad,
            'id_categoria': self.id_categoria,
            'flag_estado': self.flag_estado,
            # Opcional: incluir datos de relaciones
            'unidad_nombre': self.unidad.nombre_unidad if self.unidad else None,
            'categoria_nombre': self.categoria.nombre_categoria if self.categoria else None
        }