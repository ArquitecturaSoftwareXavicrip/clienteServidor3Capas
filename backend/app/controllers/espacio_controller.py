from flask import Blueprint, request, jsonify
from app.services.espacio_service import EspacioService

espacio_bp = Blueprint('espacio', __name__, url_prefix='/api/espacios')

@espacio_bp.route('', methods=['GET'])
def get_all_espacios():
    """Obtiene todos los espacios, opcionalmente filtrados por empresa"""
    try:
        empresa_id = request.args.get('empresa_id')
        if empresa_id:
            espacios = EspacioService.get_espacios_by_empresa(empresa_id)
        else:
            espacios = EspacioService.get_all_espacios()
            
        return jsonify([espacio.to_dict() for espacio in espacios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@espacio_bp.route('/<int:espacio_id>', methods=['GET'])
def get_espacio(espacio_id):
    """Obtiene un espacio por ID"""
    try:
        espacio = EspacioService.get_espacio_by_id(espacio_id)
        if not espacio:
            return jsonify({'error': 'Espacio no encontrado'}), 404
        return jsonify(espacio.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@espacio_bp.route('', methods=['POST'])
def create_espacio():
    """Crea un nuevo espacio"""
    try:
        data = request.get_json()
        espacio = EspacioService.create_espacio(data)
        return jsonify(espacio.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@espacio_bp.route('/<int:espacio_id>', methods=['PUT'])
def update_espacio(espacio_id):
    """Actualiza un espacio"""
    try:
        data = request.get_json()
        espacio = EspacioService.update_espacio(espacio_id, data)
        if not espacio:
            return jsonify({'error': 'Espacio no encontrado'}), 404
        return jsonify(espacio.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@espacio_bp.route('/<int:espacio_id>', methods=['DELETE'])
def delete_espacio(espacio_id):
    """Elimina un espacio"""
    try:
        result = EspacioService.delete_espacio(espacio_id)
        if not result:
            return jsonify({'error': 'Espacio no encontrado'}), 404
        return jsonify({'message': 'Espacio eliminado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
