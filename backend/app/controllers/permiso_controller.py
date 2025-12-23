"""
Controlador de Permiso - Tier 2: Lógica de Negocio (MVC)
Maneja las peticiones HTTP relacionadas con Permiso
"""
from flask import Blueprint, request, jsonify
from app.services.permiso_service import PermisoService

permiso_bp = Blueprint('permiso', __name__, url_prefix='/api/permisos')

@permiso_bp.route('', methods=['GET'])
def get_all_permisos():
    """Obtiene todos los permisos"""
    try:
        # Verificar si hay filtro por estado
        estado = request.args.get('estado')
        if estado:
            permisos = PermisoService.get_permisos_by_estado(estado)
        else:
            permisos = PermisoService.get_all_permisos()
        
        return jsonify([permiso.to_dict() for permiso in permisos]), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@permiso_bp.route('/<int:permiso_id>', methods=['GET'])
def get_permiso(permiso_id):
    """Obtiene un permiso por ID"""
    try:
        permiso = PermisoService.get_permiso_by_id(permiso_id)
        if not permiso:
            return jsonify({'error': 'Permiso no encontrado'}), 404
        return jsonify(permiso.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@permiso_bp.route('', methods=['POST'])
def create_permiso():
    """Crea un nuevo permiso"""
    try:
        data = request.get_json()
        permiso = PermisoService.create_permiso(data)
        return jsonify(permiso.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@permiso_bp.route('/<int:permiso_id>', methods=['PUT'])
def update_permiso(permiso_id):
    """Actualiza un permiso"""
    try:
        data = request.get_json()
        permiso = PermisoService.update_permiso(permiso_id, data)
        if not permiso:
            return jsonify({'error': 'Permiso no encontrado'}), 404
        return jsonify(permiso.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@permiso_bp.route('/<int:permiso_id>', methods=['DELETE'])
def delete_permiso(permiso_id):
    """Elimina un permiso"""
    try:
        result = PermisoService.delete_permiso(permiso_id)
        if not result:
            return jsonify({'error': 'Permiso no encontrado'}), 404
        return jsonify({'message': 'Permiso eliminado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@permiso_bp.route('/<int:permiso_id>/aprobar', methods=['POST'])
def aprobar_permiso(permiso_id):
    """Aprueba un permiso"""
    try:
        data = request.get_json() or {}
        observaciones = data.get('observaciones')
        permiso = PermisoService.aprobar_permiso(permiso_id, observaciones)
        return jsonify(permiso.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@permiso_bp.route('/<int:permiso_id>/rechazar', methods=['POST'])
def rechazar_permiso(permiso_id):
    """Rechaza un permiso"""
    try:
        data = request.get_json() or {}
        observaciones = data.get('observaciones')
        permiso = PermisoService.rechazar_permiso(permiso_id, observaciones)
        return jsonify(permiso.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

