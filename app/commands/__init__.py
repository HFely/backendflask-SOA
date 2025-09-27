# app/commands/__init__.py
from flask import current_app
from app.extensions import db

def register_commands(app):
    """Registrar todos los comandos CLI"""
    from .data_commands import register_data_commands
    register_data_commands(app)