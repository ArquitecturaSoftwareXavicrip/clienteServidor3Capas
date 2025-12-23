"""
Modelo de dominio Permiso - Tier 3: Acceso a Datos
"""
from app.config.database import db

class Permiso(db.Model):
    """Modelo que representa un permiso de vacaciones"""
    __tablename__ = 'permisos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False, default='Vacaciones')
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    dias_solicitados = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')  # pendiente, aprobado, rechazado
    observaciones = db.Column(db.Text)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'empleado': self.empleado,
            'tipo': self.tipo,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'dias_solicitados': self.dias_solicitados,
            'estado': self.estado,
            'observaciones': self.observaciones
        }
    
    def __repr__(self):
        return f'<Permiso {self.empleado} - {self.tipo}>'

