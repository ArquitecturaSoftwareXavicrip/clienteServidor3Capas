"""
Repositorio de Empresa - Tier 3: Acceso a Datos
Encapsula todas las operaciones de acceso a datos para Empresa
"""
from app.config.database import db
from app.models.empresa import Empresa

class EmpresaRepository:
    """Repositorio para operaciones CRUD de Empresa"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las empresas"""
        return Empresa.query.all()
    
    @staticmethod
    def get_by_id(empresa_id):
        """Obtiene una empresa por su ID"""
        return Empresa.query.get(empresa_id)
    
    @staticmethod
    def create(empresa_data):
        """Crea una nueva empresa"""
        empresa = Empresa(
            nombre=empresa_data['nombre'],
            direccion=empresa_data['direccion'],
            telefono=empresa_data['telefono'],
            email=empresa_data['email']
        )
        db.session.add(empresa)
        db.session.commit()
        return empresa
    
    @staticmethod
    def update(empresa_id, empresa_data):
        """Actualiza una empresa existente"""
        empresa = EmpresaRepository.get_by_id(empresa_id)
        if not empresa:
            return None
        
        empresa.nombre = empresa_data.get('nombre', empresa.nombre)
        empresa.direccion = empresa_data.get('direccion', empresa.direccion)
        empresa.telefono = empresa_data.get('telefono', empresa.telefono)
        empresa.email = empresa_data.get('email', empresa.email)
        
        db.session.commit()
        return empresa
    
    @staticmethod
    def delete(empresa_id):
        """Elimina una empresa"""
        empresa = EmpresaRepository.get_by_id(empresa_id)
        if not empresa:
            return False
        
        db.session.delete(empresa)
        db.session.commit()
        return True


