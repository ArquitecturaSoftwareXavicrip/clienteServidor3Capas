from flask import Blueprint, request, jsonify
from app.services.asignacion_service import AsignacionService

asignacion_bp = Blueprint('asignacion', __name__, url_prefix='/api/asignaciones')

@asignacion_bp.route('', methods=['GET'])
def get_all_asignaciones():
    """Obtiene todas las asignaciones"""
    try:
        asignaciones = AsignacionService.get_all_asignaciones()
        return jsonify([asignacion.to_dict() for asignacion in asignaciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@asignacion_bp.route('/<int:asignacion_id>', methods=['GET'])
def get_asignacion(asignacion_id):
    """Obtiene una asignacion por ID"""
    try:
        asignacion = AsignacionService.get_asignacion_by_id(asignacion_id)
        if not asignacion:
            return jsonify({'error': 'Asignacion no encontrada'}), 404
        return jsonify(asignacion.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@asignacion_bp.route('', methods=['POST'])
def create_asignacion():
    """Crea una nueva asignacion"""
    try:
        data = request.get_json()
        asignacion = AsignacionService.create_asignacion(data)
        return jsonify(asignacion.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@asignacion_bp.route('/<int:asignacion_id>', methods=['PUT'])
def update_asignacion(asignacion_id):
    """Actualiza una asignacion"""
    try:
        data = request.get_json()
        asignacion = AsignacionService.update_asignacion(asignacion_id, data)
        if not asignacion:
            return jsonify({'error': 'Asignacion no encontrada'}), 404
        return jsonify(asignacion.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@asignacion_bp.route('/<int:asignacion_id>', methods=['DELETE'])
def delete_asignacion(asignacion_id):
    """Elimina una asignacion"""
    try:
        result = AsignacionService.delete_asignacion(asignacion_id)
        if not result:
            return jsonify({'error': 'Asignacion no encontrada'}), 404
        return jsonify({'message': 'Asignacion eliminada correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
