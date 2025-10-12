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
    
    def to_dict(self):
        return {
            'id_entidad': self.id_entidad,
            'nombre_entidad': self.nombre_entidad,
            'id_tipo_doc_ident': self.id_tipo_doc_ident,
            'nro_doc_ident': self.nro_doc_ident,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'flag_proveedor': self.flag_proveedor,
            'flag_cliente': self.flag_cliente,
            'flag_estado': self.flag_estado,
            # Información de relaciones (opcional pero muy útil)
            'tipo_documento_nombre': self.tipo_documento.nombre_tipo_doc_ident if self.tipo_documento else None
        }