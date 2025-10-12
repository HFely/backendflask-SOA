# app/routes/reportes.py
from flask import Blueprint, jsonify
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.vale_almacen import ValeAlmacen
from app.extensions import db
from app.decorators.PyJWT import token_required
from sqlalchemy import func
from datetime import datetime

reportes_bp = Blueprint('reportes', __name__)

# Crear archivo pdf de reporte global en cantidad de las tablas
@reportes_bp.route('/reportes/resumen', methods=['GET'])
@token_required
def ReporteResumen(current_user):
    try:
        # Contar total de usuarios
        total_usuarios = db.session.query(func.count(Usuario.id_user)).scalar()
        
        # Contar total de categorías
        total_categorias = db.session.query(func.count(Categoria.id_categoria)).scalar()
        
        # Contar total de vales de almacén
        total_vales = db.session.query(func.count(ValeAlmacen.id_vale_almacen)).scalar()
        
        # Obtener la fecha y hora actual
        fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        reporte = {
            'total_usuarios': total_usuarios,
            'total_categorias': total_categorias,
            'total_vales_almacen': total_vales,
            'fecha_reporte': fecha_reporte
        }
        
        return jsonify(reporte), 200
    except Exception as e:
        return jsonify({"message": "Error al generar el reporte", "error": str(e)}), 500
    
# Crear archivo excel de reporte global en cantidad de las tablas
@reportes_bp.route('/reportes/resumen_excel', methods=['GET'])
@token_required
def ReporteResumenExcel(current_user):
    try:
        # Contar total de usuarios
        total_usuarios = db.session.query(func.count(Usuario.id_user)).scalar()
        
        # Contar total de categorías
        total_categorias = db.session.query(func.count(Categoria.id_categoria)).scalar()
        
        # Contar total de vales de almacén
        total_vales = db.session.query(func.count(ValeAlmacen.id_vale_almacen)).scalar()
        
        # Obtener la fecha y hora actual
        fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        reporte = {
            'total_usuarios': total_usuarios,
            'total_categorias': total_categorias,
            'total_vales_almacen': total_vales,
            'fecha_reporte': fecha_reporte
        }
        
        return jsonify(reporte), 200
    except Exception as e:
        return jsonify({"message": "Error al generar el reporte", "error": str(e)}), 500
    
