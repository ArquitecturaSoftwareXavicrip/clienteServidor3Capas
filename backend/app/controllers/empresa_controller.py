"""
Controlador de Empresa - Tier 2: Lógica de Negocio (MVC)
Maneja las peticiones HTTP relacionadas con Empresa
"""
from flask import Blueprint, request, jsonify
from app.services.empresa_service import EmpresaService

empresa_bp = Blueprint('empresa', __name__, url_prefix='/api/empresas')

@empresa_bp.route('', methods=['GET'])
def get_all_empresas():
    """Obtiene todas las empresas"""
    try:
        empresas = EmpresaService.get_all_empresas()
        return jsonify([empresa.to_dict() for empresa in empresas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empresa_bp.route('/<int:empresa_id>', methods=['GET'])
def get_empresa(empresa_id):
    """Obtiene una empresa por ID"""
    try:
        empresa = EmpresaService.get_empresa_by_id(empresa_id)
        if not empresa:
            return jsonify({'error': 'Empresa no encontrada'}), 404
        return jsonify(empresa.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empresa_bp.route('', methods=['POST'])
def create_empresa():
    """Crea una nueva empresa"""
    try:
        data = request.get_json()
        empresa = EmpresaService.create_empresa(data)
        return jsonify(empresa.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empresa_bp.route('/<int:empresa_id>', methods=['PUT'])
def update_empresa(empresa_id):
    """Actualiza una empresa"""
    try:
        data = request.get_json()
        empresa = EmpresaService.update_empresa(empresa_id, data)
        if not empresa:
            return jsonify({'error': 'Empresa no encontrada'}), 404
        return jsonify(empresa.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empresa_bp.route('/<int:empresa_id>', methods=['DELETE'])
def delete_empresa(empresa_id):
    """Elimina una empresa"""
    try:
        result = EmpresaService.delete_empresa(empresa_id)
        if not result:
            return jsonify({'error': 'Empresa no encontrada'}), 404
        return jsonify({'message': 'Empresa eliminada correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


