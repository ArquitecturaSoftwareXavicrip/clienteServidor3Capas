"""
Repositorio de Contrato - Tier 3: Acceso a Datos
Encapsula todas las operaciones de acceso a datos para Contrato
"""
from app.config.database import db
from app.models.contrato import Contrato
from datetime import datetime

class ContratoRepository:
    """Repositorio para operaciones CRUD de Contrato"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los contratos"""
        return Contrato.query.all()
    
    @staticmethod
    def get_by_id(contrato_id):
        """Obtiene un contrato por su ID"""
        return Contrato.query.get(contrato_id)
    
    @staticmethod
    def create(contrato_data):
        """Crea un nuevo contrato"""
        fecha_inicio = datetime.strptime(contrato_data['fecha_inicio'], '%Y-%m-%d').date()
        fecha_fin = None
        if contrato_data.get('fecha_fin'):
            fecha_fin = datetime.strptime(contrato_data['fecha_fin'], '%Y-%m-%d').date()
        
        contrato = Contrato(
            empresa_id=contrato_data['empresa_id'],
            servicio_id=contrato_data['servicio_id'],
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=contrato_data.get('estado', 'activo'),
            precio_final=contrato_data['precio_final']
        )
        db.session.add(contrato)
        db.session.commit()
        return contrato
    
    @staticmethod
    def update(contrato_id, contrato_data):
        """Actualiza un contrato existente"""
        contrato = ContratoRepository.get_by_id(contrato_id)
        if not contrato:
            return None
        
        if 'empresa_id' in contrato_data:
            contrato.empresa_id = contrato_data['empresa_id']
        if 'servicio_id' in contrato_data:
            contrato.servicio_id = contrato_data['servicio_id']
        if 'fecha_inicio' in contrato_data:
            contrato.fecha_inicio = datetime.strptime(contrato_data['fecha_inicio'], '%Y-%m-%d').date()
        if 'fecha_fin' in contrato_data:
            if contrato_data['fecha_fin']:
                contrato.fecha_fin = datetime.strptime(contrato_data['fecha_fin'], '%Y-%m-%d').date()
            else:
                contrato.fecha_fin = None
        if 'estado' in contrato_data:
            contrato.estado = contrato_data['estado']
        if 'precio_final' in contrato_data:
            contrato.precio_final = contrato_data['precio_final']
        
        db.session.commit()
        return contrato
    
    @staticmethod
    def delete(contrato_id):
        """Elimina un contrato"""
        contrato = ContratoRepository.get_by_id(contrato_id)
        if not contrato:
            return False
        
        db.session.delete(contrato)
        db.session.commit()
        return True



