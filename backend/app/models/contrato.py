"""
Modelo de dominio Contrato - Tier 3: Acceso a Datos
"""
from app.config.database import db
from datetime import datetime

class Contrato(db.Model):
    """Modelo que representa un contrato entre empresa y servicio"""
    __tablename__ = 'contratos'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    estado = db.Column(db.String(20), nullable=False, default='activo')  # activo, finalizado, cancelado
    precio_final = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'empresa_id': self.empresa_id,
            'servicio_id': self.servicio_id,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'estado': self.estado,
            'precio_final': self.precio_final,
            'empresa': self.empresa.to_dict() if self.empresa else None,
            'servicio': self.servicio.to_dict() if self.servicio else None
        }
    
    def __repr__(self):
        return f'<Contrato {self.id} - Empresa: {self.empresa_id}, Servicio: {self.servicio_id}>'



