# app/commands/data_commands.py
from app.scripts.init_data import init_tipo_doc_ident
from app.utils.data_checker import ensure_essential_data

def register_data_commands(app):
    """Registrar comandos relacionados con datos"""
    
    @app.cli.command("init-data")
    def init_data_command():
        """Inicializar datos por defecto en la base de datos"""
        init_tipo_doc_ident()
        print("Datos inicializados correctamente")
    
    @app.cli.command("check-data")
    def check_data_command():
        """Verificar datos esenciales"""
        if ensure_essential_data():
            print("Datos esenciales verificados")
        else:
            print("Faltan datos esenciales")