from flask import Blueprint, request, jsonify
from app.services.prestamo_service import PrestamoService

prestamo_bp = Blueprint('prestamo', __name__, url_prefix='/api/prestamos')

@prestamo_bp.route('', methods=['GET'])
def get_all():
    items = PrestamoService.get_all()
    return jsonify([i.to_dict() for i in items]), 200

@prestamo_bp.route('/<int:id>', methods=['GET'])
def get_one(id):
    item = PrestamoService.get_by_id(id)
    return jsonify(item.to_dict()) if item else (jsonify({'error': 'No encontrado'}), 404)

@prestamo_bp.route('', methods=['POST'])
def create():
    try:
        data = request.get_json()
        item = PrestamoService.create(data)
        return jsonify(item.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@prestamo_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    item = PrestamoService.update(id, data)
    return jsonify(item.to_dict()) if item else (jsonify({'error': 'No encontrado'}), 404)

@prestamo_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    success = PrestamoService.delete(id)
    return jsonify({'message': 'Eliminado'}) if success else (jsonify({'error': 'No encontrado'}), 404)