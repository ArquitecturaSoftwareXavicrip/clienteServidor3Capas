from app.config.database import db

class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    
    id = db.Column(db.Integer, primary_key=True)
    equipo = db.Column(db.String(100), nullable=False) # Coincide con el frontend
    fecha_prestamo = db.Column(db.String(20), nullable=False) # Almacenado como string (YYYY-MM-DD)
    
    def to_dict(self):
        return {
            'id': self.id,
            'equipo': self.equipo,
            'fecha_prestamo': self.fecha_prestamo
        }