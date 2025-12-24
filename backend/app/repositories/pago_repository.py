
from app.config.database import db
from app.models.pago import Pago

class PagoRepository:
    @staticmethod
    def create(pago_data):
        # El cálculo del total se hace aquí o en el servicio
        total = pago_data['monto_base'] + pago_data.get('extras', 0)
        nuevo_pago = Pago(
            empleado_id=pago_data['empleado_id'],
            monto_base=pago_data['monto_base'],
            extras=pago_data.get('extras', 0),
            monto_total=total
        )
        db.session.add(nuevo_pago)
        db.session.commit()
        return nuevo_pago

    @staticmethod
    def get_by_empleado(empleado_id):
        return Pago.query.filter_by(empleado_id=empleado_id).all()