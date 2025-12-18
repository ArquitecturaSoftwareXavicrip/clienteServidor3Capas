"""
Controlador de Contrato - Tier 2: Lógica de Negocio (MVC)
Maneja las peticiones HTTP relacionadas con Contrato
"""
from flask import Blueprint, request, jsonify
from app.services.contrato_service import ContratoService

contrato_bp = Blueprint('contrato', __name__, url_prefix='/api/contratos')

@contrato_bp.route('', methods=['GET'])
def get_all_contratos():
    """Obtiene todos los contratos"""
    try:
        contratos = ContratoService.get_all_contratos()
        return jsonify([contrato.to_dict() for contrato in contratos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contrato_bp.route('/<int:contrato_id>', methods=['GET'])
def get_contrato(contrato_id):
    """Obtiene un contrato por ID"""
    try:
        contrato = ContratoService.get_contrato_by_id(contrato_id)
        if not contrato:
            return jsonify({'error': 'Contrato no encontrado'}), 404
        return jsonify(contrato.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contrato_bp.route('', methods=['POST'])
def create_contrato():
    """Crea un nuevo contrato"""
    try:
        data = request.get_json()
        contrato = ContratoService.create_contrato(data)
        return jsonify(contrato.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contrato_bp.route('/<int:contrato_id>', methods=['PUT'])
def update_contrato(contrato_id):
    """Actualiza un contrato"""
    try:
        data = request.get_json()
        contrato = ContratoService.update_contrato(contrato_id, data)
        if not contrato:
            return jsonify({'error': 'Contrato no encontrado'}), 404
        return jsonify(contrato.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contrato_bp.route('/<int:contrato_id>', methods=['DELETE'])
def delete_contrato(contrato_id):
    """Elimina un contrato"""
    try:
        result = ContratoService.delete_contrato(contrato_id)
        if not result:
            return jsonify({'error': 'Contrato no encontrado'}), 404
        return jsonify({'message': 'Contrato eliminado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


