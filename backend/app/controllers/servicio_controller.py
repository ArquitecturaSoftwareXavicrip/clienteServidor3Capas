"""
Controlador de Servicio - Tier 2: Lógica de Negocio (MVC)
Maneja las peticiones HTTP relacionadas con Servicio
"""
from flask import Blueprint, request, jsonify
from app.services.servicio_service import ServicioService

servicio_bp = Blueprint('servicio', __name__, url_prefix='/api/servicios')

@servicio_bp.route('', methods=['GET'])
def get_all_servicios():
    """Obtiene todos los servicios"""
    try:
        servicios = ServicioService.get_all_servicios()
        return jsonify([servicio.to_dict() for servicio in servicios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicio_bp.route('/<int:servicio_id>', methods=['GET'])
def get_servicio(servicio_id):
    """Obtiene un servicio por ID"""
    try:
        servicio = ServicioService.get_servicio_by_id(servicio_id)
        if not servicio:
            return jsonify({'error': 'Servicio no encontrado'}), 404
        return jsonify(servicio.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicio_bp.route('', methods=['POST'])
def create_servicio():
    """Crea un nuevo servicio"""
    try:
        data = request.get_json()
        servicio = ServicioService.create_servicio(data)
        return jsonify(servicio.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicio_bp.route('/<int:servicio_id>', methods=['PUT'])
def update_servicio(servicio_id):
    """Actualiza un servicio"""
    try:
        data = request.get_json()
        servicio = ServicioService.update_servicio(servicio_id, data)
        if not servicio:
            return jsonify({'error': 'Servicio no encontrado'}), 404
        return jsonify(servicio.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicio_bp.route('/<int:servicio_id>', methods=['DELETE'])
def delete_servicio(servicio_id):
    """Elimina un servicio"""
    try:
        result = ServicioService.delete_servicio(servicio_id)
        if not result:
            return jsonify({'error': 'Servicio no encontrado'}), 404
        return jsonify({'message': 'Servicio eliminado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


