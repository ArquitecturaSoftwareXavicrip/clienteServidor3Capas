"""
Modelo de dominio Empresa - Tier 3: Acceso a Datos
"""
from app.config.database import db

class Empresa(db.Model):
    """Modelo que representa una empresa cliente"""
    __tablename__ = 'empresas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    
    # Relación con contratos
    contratos = db.relationship('Contrato', backref='empresa', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email
        }
    
    def __repr__(self):
        return f'<Empresa {self.nombre}>'



