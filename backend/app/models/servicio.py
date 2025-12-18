"""
Modelo de dominio Servicio - Tier 3: Acceso a Datos
"""
from app.config.database import db

class Servicio(db.Model):
    """Modelo que representa un servicio de limpieza"""
    __tablename__ = 'servicios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio_base = db.Column(db.Float, nullable=False)
    duracion_horas = db.Column(db.Float, nullable=False)
    
    # Relación con contratos
    contratos = db.relationship('Contrato', backref='servicio', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_base': self.precio_base,
            'duracion_horas': self.duracion_horas
        }
    
    def __repr__(self):
        return f'<Servicio {self.nombre}>'


