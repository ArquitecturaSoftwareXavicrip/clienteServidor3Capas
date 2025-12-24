from app.config.database import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'pagos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    monto_base = db.Column(db.Float, nullable=False)
    extras = db.Column(db.Float, default=0.0)
    monto_total = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'empleado_id': self.empleado_id,
            'monto_base': self.monto_base,
            'extras': self.extras,
            'monto_total': self.monto_total,
            'fecha_pago': self.fecha_pago.strftime('%Y-%m-%d')
        }