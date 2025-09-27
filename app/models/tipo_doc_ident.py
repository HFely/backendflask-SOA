# app/models/tipo_doc_ident.py
from app.extensions import db

# Tabla donde se registran los tipos de documentos de identificación (Ejemplo: DNI, RUC, Carnet de Extranjería, Pasaporte, etc.)
# Tabla donde se registra los tipos de documentos de identidad de personas o empresas
class TipoDocIdent(db.Model):
    __tablename__ = 'tipo_doc_ident'
    
    id_tipo_doc_ident = db.Column(db.Integer, primary_key=True)
    nombre_tipo_doc_ident = db.Column(db.String(30), nullable=False)
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    def __repr__(self):
        return f'<TipoDocIdent {self.nombre_tipo_doc_ident}>'