from app.config.database import db
from app.models.espacio import Espacio

class EspacioRepository:
    """Repositorio para operaciones CRUD de Espacio"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los espacios"""
        return Espacio.query.all()
    
    @staticmethod
    def get_by_id(espacio_id):
        """Obtiene un espacio por su ID"""
        return Espacio.query.get(espacio_id)
    
    @staticmethod
    def get_by_empresa(empresa_id):
        """Obtiene todos los espacios de una empresa"""
        return Espacio.query.filter_by(empresa_id=empresa_id).all()
        
    @staticmethod
    def create(data):
        """Crea un nuevo espacio"""
        espacio = Espacio(
            nombre=data['nombre'],
            tipo=data['tipo'],
            empresa_id=data['empresa_id'],
            observaciones=data.get('observaciones')
        )
        db.session.add(espacio)
        db.session.commit()
        return espacio
    
    @staticmethod
    def update(espacio_id, data):
        """Actualiza un espacio existente"""
        espacio = EspacioRepository.get_by_id(espacio_id)
        if not espacio:
            return None
        
        espacio.nombre = data.get('nombre', espacio.nombre)
        espacio.tipo = data.get('tipo', espacio.tipo)
        espacio.empresa_id = data.get('empresa_id', espacio.empresa_id)
        espacio.observaciones = data.get('observaciones', espacio.observaciones)
        
        db.session.commit()
        return espacio
    
    @staticmethod
    def delete(espacio_id):
        """Elimina un espacio"""
        espacio = EspacioRepository.get_by_id(espacio_id)
        if not espacio:
            return False
        
        db.session.delete(espacio)
        db.session.commit()
        return True
