# app/__init__.py
from flask import Flask
from app.commands import register_commands
from config import config
from .extensions import db, migrate, jwt
from app.routes import register_blueprints

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    register_blueprints(app)
    register_commands(app)
    
    return app