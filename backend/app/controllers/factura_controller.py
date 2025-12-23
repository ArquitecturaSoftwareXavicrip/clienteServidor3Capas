"""
Controlador de Factura - Tier 2: Lógica de Negocio (MVC)
Maneja las peticiones HTTP relacionadas con Factura
"""
from flask import Blueprint, request, jsonify
from app.services.factura_service import FacturaService

factura_bp = Blueprint('factura', __name__, url_prefix='/api/facturas')

@factura_bp.route('', methods=['GET'])
def get_all_facturas():
    """Obtiene todas las facturas"""
    try:
        facturas = FacturaService.get_all_facturas()
        return jsonify([factura.to_dict() for factura in facturas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@factura_bp.route('/<int:factura_id>', methods=['GET'])
def get_factura(factura_id):
    """Obtiene una factura por ID"""
    try:
        factura = FacturaService.get_factura_by_id(factura_id)
        if not factura:
            return jsonify({'error': 'Factura no encontrada'}), 404
        return jsonify(factura.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@factura_bp.route('/empresa/<int:empresa_id>', methods=['GET'])
def get_facturas_by_empresa(empresa_id):
    """Obtiene todas las facturas de una empresa"""
    try:
        facturas = FacturaService.get_facturas_by_empresa(empresa_id)
        return jsonify([factura.to_dict() for factura in facturas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@factura_bp.route('', methods=['POST'])
def create_factura():
    """Crea una nueva factura"""
    try:
        data = request.get_json()
        factura = FacturaService.create_factura(data)
        return jsonify(factura.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@factura_bp.route('/<int:factura_id>', methods=['PUT'])
def update_factura(factura_id):
    """Actualiza una factura"""
    try:
        data = request.get_json()
        factura = FacturaService.update_factura(factura_id, data)
        if not factura:
            return jsonify({'error': 'Factura no encontrada'}), 404
        return jsonify(factura.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@factura_bp.route('/<int:factura_id>', methods=['DELETE'])
def delete_factura(factura_id):
    """Elimina una factura"""
    try:
        result = FacturaService.delete_factura(factura_id)
        if not result:
            return jsonify({'error': 'Factura no encontrada'}), 404
        return jsonify({'message': 'Factura eliminada correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
