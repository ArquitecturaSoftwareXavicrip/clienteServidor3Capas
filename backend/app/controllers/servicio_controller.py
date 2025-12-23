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
        return jsonify([s.to_dict() for s in servicios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@servicio_bp.route('/<int:servicio_id>', methods=['GET'])
def get_servicio(servicio_id: int):
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
    if not request.is_json:
        return jsonify({'error': 'Se requiere payload JSON'}), 400

    try:
        data = request.get_json()
        servicio = ServicioService.create_servicio(data)
        return jsonify(servicio.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@servicio_bp.route('/<int:servicio_id>', methods=['PUT'])
def update_servicio(servicio_id: int):
    """Actualiza un servicio"""
    if not request.is_json:
        return jsonify({'error': 'Se requiere payload JSON'}), 400

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
def delete_servicio(servicio_id: int):
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


@servicio_bp.route('/<int:servicio_id>/asignar', methods=['POST'])
def asignar_empleado_a_servicio(servicio_id: int):
    """Asigna un empleado a un servicio (body JSON: { "empleado_id": <int> })"""
    if not request.is_json:
        return jsonify({'error': 'Se requiere payload JSON'}), 400

    data = request.get_json()
    empleado_id = data.get('empleado_id')
    if empleado_id is None:
        return jsonify({'error': 'Empleado ID es requerido'}), 400

    try:
        servicio = ServicioService.asignar_empleado(servicio_id, empleado_id)
        if servicio:
            return jsonify(servicio.to_dict()), 200
        return jsonify({'error': 'Servicio o Empleado no encontrado'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@servicio_bp.route('/<int:servicio_id>/desasignar', methods=['POST'])
def desasignar_empleado_de_servicio(servicio_id: int):
    """Desasigna un empleado de un servicio (body JSON: { "empleado_id": <int> })"""
    if not request.is_json:
        return jsonify({'error': 'Se requiere payload JSON'}), 400

    data = request.get_json()
    empleado_id = data.get('empleado_id')
    if empleado_id is None:
        return jsonify({'error': 'Empleado ID es requerido'}), 400

    try:
        servicio = ServicioService.desasignar_empleado(servicio_id, empleado_id)
        if servicio:
            return jsonify(servicio.to_dict()), 200
        return jsonify({'error': 'Servicio o Empleado no encontrado'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
