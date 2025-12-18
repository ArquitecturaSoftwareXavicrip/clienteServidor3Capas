"""
Repositorio de Servicio - Tier 3: Acceso a Datos
Encapsula todas las operaciones de acceso a datos para Servicio
"""
from app.config.database import db
from app.models.servicio import Servicio

class ServicioRepository:
    """Repositorio para operaciones CRUD de Servicio"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los servicios"""
        return Servicio.query.all()
    
    @staticmethod
    def get_by_id(servicio_id):
        """Obtiene un servicio por su ID"""
        return Servicio.query.get(servicio_id)
    
    @staticmethod
    def create(servicio_data):
        """Crea un nuevo servicio"""
        servicio = Servicio(
            nombre=servicio_data['nombre'],
            descripcion=servicio_data.get('descripcion'),
            precio_base=servicio_data['precio_base'],
            duracion_horas=servicio_data['duracion_horas']
        )
        db.session.add(servicio)
        db.session.commit()
        return servicio
    
    @staticmethod
    def update(servicio_id, servicio_data):
        """Actualiza un servicio existente"""
        servicio = ServicioRepository.get_by_id(servicio_id)
        if not servicio:
            return None
        
        servicio.nombre = servicio_data.get('nombre', servicio.nombre)
        servicio.descripcion = servicio_data.get('descripcion', servicio.descripcion)
        servicio.precio_base = servicio_data.get('precio_base', servicio.precio_base)
        servicio.duracion_horas = servicio_data.get('duracion_horas', servicio.duracion_horas)
        
        db.session.commit()
        return servicio
    
    @staticmethod
    def delete(servicio_id):
        """Elimina un servicio"""
        servicio = ServicioRepository.get_by_id(servicio_id)
        if not servicio:
            return False
        
        db.session.delete(servicio)
        db.session.commit()
        return True


