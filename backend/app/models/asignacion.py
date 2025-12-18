from app.config.database import db

class Asignacion(db.Model):
    """Modelo que representa la asignación de un empleado a un espacio/servicio"""
    __tablename__ = 'asignaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacios.id'), nullable=False)
    
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)  # Si es null, es indefinido
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    frecuencia = db.Column(db.String(20), nullable=False)  # DIARIO, SEMANAL, UNICA
    estado = db.Column(db.String(20), nullable=False, default='ACTIVO')
    
    # Relaciones
    contrato = db.relationship('Contrato')
    servicio = db.relationship('Servicio')
    empleado = db.relationship('Empleado')
    espacio = db.relationship('Espacio')
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'contrato_id': self.contrato_id,
            'servicio_id': self.servicio_id,
            'empleado_id': self.empleado_id,
            'espacio_id': self.espacio_id,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'hora_inicio': self.hora_inicio.isoformat() if self.hora_inicio else None,
            'hora_fin': self.hora_fin.isoformat() if self.hora_fin else None,
            'frecuencia': self.frecuencia,
            'estado': self.estado,
            'empleado_nombre': f"{self.empleado.nombre} {self.empleado.apellido}" if self.empleado else None,
            'espacio_nombre': self.espacio.nombre if self.espacio else None,
            'servicio_nombre': self.servicio.nombre if self.servicio else None
        }
