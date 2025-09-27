# app/models/entidad_relacion.py
from app.extensions import db

# Tabla donde se registra los clientes y proveedores (entidad de relación del sistema)
class EntidadRelacion(db.Model):
    __tablename__ = 'entidad_relacion'
    
    id_entidad = db.Column(db.Integer, primary_key=True)
    nombre_entidad = db.Column(db.String(120), nullable=False, unique=True)
    id_tipo_doc_ident = db.Column(db.Integer, db.ForeignKey('tipo_doc_ident.id_tipo_doc_ident'), nullable=False)
    nro_doc_ident = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(120))
    telefono = db.Column(db.String(30))
    flag_proveedor = db.Column(db.String(1), nullable=False, default='0')
    flag_cliente = db.Column(db.String(1), nullable=False, default='0')
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    # Relaciones
    tipo_documento = db.relationship('TipoDocIdent', backref='entidades')
    
    def __repr__(self):
        return f'<EntidadRelacion {self.nombre_entidad}>'