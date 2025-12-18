"""
Servicio de Empresa - Tier 2: Lógica de Negocio
Contiene la lógica de negocio y validaciones para Empresa
"""
from app.repositories.empresa_repository import EmpresaRepository

class EmpresaService:
    """Servicio que contiene la lógica de negocio para Empresa"""
    
    @staticmethod
    def get_all_empresas():
        """Obtiene todas las empresas"""
        return EmpresaRepository.get_all()
    
    @staticmethod
    def get_empresa_by_id(empresa_id):
        """Obtiene una empresa por ID"""
        return EmpresaRepository.get_by_id(empresa_id)
    
    @staticmethod
    def create_empresa(empresa_data):
        """Crea una nueva empresa con validaciones"""
        # Validaciones de negocio
        errors = []
        
        if not empresa_data.get('nombre') or len(empresa_data['nombre'].strip()) == 0:
            errors.append('El nombre es requerido')
        
        if not empresa_data.get('direccion') or len(empresa_data['direccion'].strip()) == 0:
            errors.append('La dirección es requerida')
        
        if not empresa_data.get('telefono') or len(empresa_data['telefono'].strip()) == 0:
            errors.append('El teléfono es requerido')
        
        if not empresa_data.get('email') or len(empresa_data['email'].strip()) == 0:
            errors.append('El email es requerido')
        elif '@' not in empresa_data['email']:
            errors.append('El email debe ser válido')
        
        if errors:
            raise ValueError('; '.join(errors))
        
        return EmpresaRepository.create(empresa_data)
    
    @staticmethod
    def update_empresa(empresa_id, empresa_data):
        """Actualiza una empresa con validaciones"""
        empresa = EmpresaRepository.get_by_id(empresa_id)
        if not empresa:
            raise ValueError('Empresa no encontrada')
        
        # Validaciones de negocio
        if 'email' in empresa_data and empresa_data['email']:
            if '@' not in empresa_data['email']:
                raise ValueError('El email debe ser válido')
        
        return EmpresaRepository.update(empresa_id, empresa_data)
    
    @staticmethod
    def delete_empresa(empresa_id):
        """Elimina una empresa"""
        empresa = EmpresaRepository.get_by_id(empresa_id)
        if not empresa:
            raise ValueError('Empresa no encontrada')
        
        return EmpresaRepository.delete(empresa_id)


