# app/models/tipo_documento.py
from app.extensions import db

#Tabla donde se registran los tipos de documentos (Ejemplo: orden de compra, guía de remisión, factura por cobrar, factura por pagar, nota de crédito, etc.)
class TipoDocumento(db.Model):
    __tablename__ = 'tipo_documento'
    
    id_tipo_documento = db.Column(db.Integer, primary_key=True)
    cod_tipo_documento = db.Column(db.String(6), unique=True, nullable=False)
    nombre_tipo_documento = db.Column(db.String(30), nullable=False)
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    def __repr__(self):
        return f'<TipoDocumento {self.cod_tipo_documento}>'