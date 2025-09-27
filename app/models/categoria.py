# app/models/categoria.py
from app.extensions import db

# Tabla donde se registran las categorías de los artículos (Ejemplo: Electrónica, Muebles, Ropa, etc.)
class Categoria(db.Model):
    __tablename__ = 'categoria'
    
    id_categoria = db.Column(db.Integer, primary_key=True)
    cod_categoria = db.Column(db.String(6), unique=True, nullable=False)
    nombre_categoria = db.Column(db.String(30), nullable=False)
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    def __repr__(self):
        return f'<Categoria {self.cod_categoria}>'