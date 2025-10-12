# app/routes/__init__.py
from .main import main_bp
from .auth import auth_bp
from .articulo import articulo_bp
from .entidad_relacion import entidad_relacion_bp
from .reportes import reportes_bp
from .usuario import usuario_bp
from .vale_almacen import vale_almacen_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(articulo_bp, url_prefix='/articulos')
    app.register_blueprint(entidad_relacion_bp, url_prefix='/entidades_relaciones')
    app.register_blueprint(reportes_bp, url_prefix='/reportes')
    app.register_blueprint(usuario_bp, url_prefix='/usuarios')
    app.register_blueprint(vale_almacen_bp, url_prefix='/vales_almacen')

# Registrar namespaces de la API
from app.routes.auth import auth_ns

def register_api_namespaces(api):
    api.add_namespace(auth_ns)