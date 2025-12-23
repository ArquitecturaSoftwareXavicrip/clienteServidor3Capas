"""
Modelo de dominio Factura - Tier 3: Acceso a Datos
"""
from app.config.database import db
from datetime import datetime

class Factura(db.Model):
    """Modelo que representa una factura de servicios"""
    __tablename__ = 'facturas'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    fecha_factura = db.Column(db.Date, nullable=False, default=datetime.now)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    impuesto = db.Column(db.Float, nullable=False, default=0.0)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')  # pendiente, pagada, cancelada
    
    # Relaciones
    empresa = db.relationship('Empresa', backref='facturas')
    servicio = db.relationship('Servicio', backref='facturas')
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'empresa_id': self.empresa_id,
            'empleado_id': self.empleado_id,
            'servicio_id': self.servicio_id,
            'fecha_factura': self.fecha_factura.isoformat() if self.fecha_factura else None,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'descripcion': self.descripcion,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal,
            'impuesto': self.impuesto,
            'total': self.total,
            'estado': self.estado,
            'empresa': self.empresa.to_dict() if self.empresa else None,
            'empleado': self.empleado.to_dict() if self.empleado else None,
            'servicio': self.servicio.to_dict() if self.servicio else None
        }
    
    def __repr__(self):
        return f'<Factura {self.id} - Empresa: {self.empresa_id}, Total: {self.total}>'
