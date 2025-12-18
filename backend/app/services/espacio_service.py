from app.repositories.espacio_repository import EspacioRepository

class EspacioService:
    """Servicio que contiene la lógica de negocio para Espacio"""
    
    @staticmethod
    def get_all_espacios():
        """Obtiene todos los espacios"""
        return EspacioRepository.get_all()
    
    @staticmethod
    def get_espacio_by_id(espacio_id):
        """Obtiene un espacio por ID"""
        return EspacioRepository.get_by_id(espacio_id)
        
    @staticmethod
    def get_espacios_by_empresa(empresa_id):
        """Obtiene espacios de una empresa específica"""
        return EspacioRepository.get_by_empresa(empresa_id)
    
    @staticmethod
    def create_espacio(data):
        """Crea un nuevo espacio con validaciones"""
        # Validaciones de negocio
        errors = []
        
        if not data.get('nombre') or len(data['nombre'].strip()) == 0:
            errors.append('El nombre es requerido')
            
        if not data.get('tipo') or len(data['tipo'].strip()) == 0:
            errors.append('El tipo es requerido')
            
        if not data.get('empresa_id'):
            errors.append('El ID de empresa es requerido')
        
        if errors:
            raise ValueError('; '.join(errors))
        
        return EspacioRepository.create(data)
    
    @staticmethod
    def update_espacio(espacio_id, data):
        """Actualiza un espacio"""
        return EspacioRepository.update(espacio_id, data)
    
    @staticmethod
    def delete_espacio(espacio_id):
        """Elimina un espacio"""
        return EspacioRepository.delete(espacio_id)
