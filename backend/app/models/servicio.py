"""
Modelo de dominio Servicio - Tier 3: Acceso a Datos
"""
from app.config.database import db

# Tabla intermedia para la relación Muchos a Muchos
asignaciones = db.Table('asignaciones',
    db.Column('servicio_id', db.Integer, db.ForeignKey('servicios.id'), primary_key=True),
    db.Column('empleado_id', db.Integer, db.ForeignKey('empleados.id'), primary_key=True)
)

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
    # NUEVO: Relación con empleados
    empleados = db.relationship('Empleado', secondary=asignaciones, lazy='subquery',
        backref=db.backref('servicios', lazy=True))
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_base': self.precio_base,
            'duracion_horas': self.duracion_horas,
            'empleados': [empleado.to_dict() for empleado in self.empleados]
        }
    
    def __repr__(self):
        return f'<Servicio {self.nombre}>'



