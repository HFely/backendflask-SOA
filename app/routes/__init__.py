# app/routes/__init__.py
from .main import main_bp
from .auth import auth_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
