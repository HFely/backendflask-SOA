# app/models/usuario.py
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla donde se registran los usuarios del sistema
class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id_user = db.Column(db.Integer, primary_key=True)
    login_user = db.Column(db.String(10), unique=True, nullable=False) # Usuario para login
    id_tipo_doc_ident = db.Column(db.Integer, db.ForeignKey('tipo_doc_ident.id_tipo_doc_ident'), nullable=False)
    nro_doc_ident = db.Column(db.String(20), nullable=False)
    nombre_user = db.Column(db.String(90), nullable=False)
    direccion_user = db.Column(db.String(120))
    telefono_user = db.Column(db.String(30))
    password = db.Column(db.String(256), nullable=False)
    flag_administrador = db.Column(db.String(1), nullable=False, default='0')
    flag_inventarios = db.Column(db.String(1), nullable=False, default='0')
    flag_estado = db.Column(db.String(1), nullable=False, default='1')
    
    # Relaciones
    tipo_documento = db.relationship('TipoDocIdent', backref='usuarios')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<Usuario {self.login_user}>'
    
    def to_dict(self):
        return {
            'id_user': self.id_user,
            'login_user': self.login_user,
            'id_tipo_doc_ident': self.id_tipo_doc_ident,
            'nro_doc_ident': self.nro_doc_ident,
            'nombre_user': self.nombre_user,
            'direccion_user': self.direccion_user,
            'telefono_user': self.telefono_user,
            'flag_administrador': self.flag_administrador,
            'flag_inventarios': self.flag_inventarios,
            'flag_estado': self.flag_estado
        }
