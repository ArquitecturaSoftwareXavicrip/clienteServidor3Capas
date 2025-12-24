from flask import Blueprint, request, jsonify
from app.services.pago_service import PagoService

pago_bp = Blueprint('pago', __name__, url_prefix='/api/pagos')

@pago_bp.route('', methods=['POST'])
def create_pago():
    try:
        data = request.get_json()
        pago = PagoService.registrar_pago(data)
        return jsonify(pago.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400