from app.config.database import db

class Espacio(db.Model):
    """Modelo que representa un espacio físico de una empresa"""
    __tablename__ = 'espacios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ej. Oficina, Baño, Hall
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    
    # Relación con la empresa
    empresa = db.relationship('Empresa', backref=db.backref('espacios', lazy=True))
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'empresa_id': self.empresa_id,
            'observaciones': self.observaciones,
            'empresa_nombre': self.empresa.nombre if self.empresa else None
        }
    
    def __repr__(self):
        return f'<Espacio {self.nombre} - {self.tipo}>'
