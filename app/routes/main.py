from flask import Blueprint, jsonify, render_template
from app.decorators.jwt_required import jwt_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return jsonify({
        "message": "Bienvenido a la API",
        "endpoints": {
            "users": "/users",
            "enterprises": "/enterprises",
            "auth": "/auth"
        }
    })

# ruta que muestre un home page sin template
@main_bp.route('/home')
def home():
    return "<h1>Home Page</h1><p>Bienvenido a la página principal de la API.</p>"
