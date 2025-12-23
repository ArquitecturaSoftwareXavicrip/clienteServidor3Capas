"""
Servicio de Servicio - Tier 2: Lógica de Negocio
Contiene la lógica de negocio y validaciones para Servicio
"""
from app.repositories.servicio_repository import ServicioRepository

class ServicioService:
    """Servicio que contiene la lógica de negocio para Servicio"""
    
    @staticmethod
    def get_all_servicios():
        """Obtiene todos los servicios"""
        return ServicioRepository.get_all()
    
    @staticmethod
    def get_servicio_by_id(servicio_id):
        """Obtiene un servicio por ID"""
        return ServicioRepository.get_by_id(servicio_id)
    
    @staticmethod
    def create_servicio(servicio_data):
        """Crea un nuevo servicio con validaciones"""
        # Validaciones de negocio
        errors = []
        
        if not servicio_data.get('nombre') or len(servicio_data['nombre'].strip()) == 0:
            errors.append('El nombre es requerido')
        
        precio_base = servicio_data.get('precio_base')
        if precio_base is None:
            errors.append('El precio base es requerido')
        elif precio_base < 0:
            errors.append('El precio base debe ser mayor o igual a 0')
        
        duracion_horas = servicio_data.get('duracion_horas')
        if duracion_horas is None:
            errors.append('La duración en horas es requerida')
        elif duracion_horas <= 0:
            errors.append('La duración debe ser mayor a 0')
        
        if errors:
            raise ValueError('; '.join(errors))
        
        return ServicioRepository.create(servicio_data)
    
    @staticmethod
    def update_servicio(servicio_id, servicio_data):
        """Actualiza un servicio con validaciones"""
        servicio = ServicioRepository.get_by_id(servicio_id)
        if not servicio:
            raise ValueError('Servicio no encontrado')
        
        # Validaciones de negocio
        if 'precio_base' in servicio_data and servicio_data['precio_base'] < 0:
            raise ValueError('El precio base debe ser mayor o igual a 0')
        
        if 'duracion_horas' in servicio_data and servicio_data['duracion_horas'] <= 0:
            raise ValueError('La duración debe ser mayor a 0')
        
        return ServicioRepository.update(servicio_id, servicio_data)
    
    @staticmethod
    def delete_servicio(servicio_id):
        """Elimina un servicio"""
        servicio = ServicioRepository.get_by_id(servicio_id)
        if not servicio:
            raise ValueError('Servicio no encontrado')
        
        return ServicioRepository.delete(servicio_id)

    @staticmethod
    def asignar_empleado(servicio_id, empleado_id):
        # Aquí podrías agregar validaciones de negocio adicionales
        # Ejemplo: Verificar si el empleado está activo o tiene capacidad
        return ServicioRepository.asignar_empleado(servicio_id, empleado_id)

    @staticmethod
    def desasignar_empleado(servicio_id, empleado_id):
        return ServicioRepository.desasignar_empleado(servicio_id, empleado_id)

