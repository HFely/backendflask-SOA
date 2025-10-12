# app/__init__.py
from flask import Flask
from app.commands import register_commands
from config import config
from .extensions import db, migrate, jwt
from app.routes import register_blueprints, register_api_namespaces
from flask_restx import Api

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Configurar Swagger/OpenAPI
    api = Api(
        app,
        version='1.3.2',
        title='API de Gestion de Inventarios',
        description='Sistema de inventarios con autenticación JWT',
        doc='/docs/',  # URL para la documentación Swagger UI
        authorizations={
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'Ingrese el token en el formato: Bearer <token>'
            }
        },
        security='Bearer Auth'
    )
    
    register_blueprints(app)
    register_api_namespaces(api)
    register_commands(app)
    
    return app