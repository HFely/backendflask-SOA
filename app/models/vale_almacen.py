# app/models/vale_almacen.py
from app.extensions import db
from datetime import datetime

#Tabla donde se registra la cabecera de un vale de almacén
class ValeAlmacen(db.Model):
    __tablename__ = 'vale_almacen'
    
    id_vale_almacen = db.Column(db.Integer, primary_key=True)
    cod_vale_almacen = db.Column(db.String(12), unique=True, nullable=False)
    id_almacen = db.Column(db.Integer, db.ForeignKey('almacen.id_almacen'), nullable=False)
    fecha_vale = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_tipo_mov_almacen = db.Column(db.Integer, db.ForeignKey('tipo_mov_almacen.id_tipo_mov_almacen'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('usuario.id_user'), nullable=False)
    id_entidad = db.Column(db.Integer, db.ForeignKey('entidad_relacion.id_entidad'))
    id_tipo_doc = db.Column(db.Integer, db.ForeignKey('tipo_documento.id_tipo_documento'))
    serie_doc = db.Column(db.String(4))
    nro_documento = db.Column(db.String(20))
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    # Relaciones
    almacen = db.relationship('Almacen', backref='vales')
    tipo_movimiento = db.relationship('TipoMovAlmacen', backref='vales')
    usuario = db.relationship('Usuario', backref='vales')
    entidad = db.relationship('EntidadRelacion', backref='vales')
    tipo_documento = db.relationship('TipoDocumento', backref='vales')
    detalles = db.relationship('ValeAlmacenDet', backref='vale', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ValeAlmacen {self.cod_vale_almacen}>'
    
    def to_dict(self):
        return {
            'id_vale_almacen': self.id_vale_almacen,
            'cod_vale_almacen': self.cod_vale_almacen,
            'id_almacen': self.id_almacen,
            'fecha_vale': self.fecha_vale.isoformat() if self.fecha_vale else None,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'id_tipo_mov_almacen': self.id_tipo_mov_almacen,
            'id_user': self.id_user,
            'id_entidad': self.id_entidad,
            'id_tipo_doc': self.id_tipo_doc,
            'serie_doc': self.serie_doc,
            'nro_documento': self.nro_documento,
            'flag_estado': self.flag_estado,
            'almacen_nombre': self.almacen.nombre_almacen if self.almacen else None,
            'tipo_movimiento_nombre': self.tipo_movimiento.nombre_tipo_mov if self.tipo_movimiento else None,
            'usuario_nombre': self.usuario.nombre_user if self.usuario else None,
            'entidad_nombre': self.entidad.nombre_entidad if self.entidad else None
        }