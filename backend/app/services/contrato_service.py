"""
Servicio de Contrato - Tier 2: Lógica de Negocio
Contiene la lógica de negocio y validaciones para Contrato
"""
from app.repositories.contrato_repository import ContratoRepository
from app.repositories.empresa_repository import EmpresaRepository
from app.repositories.servicio_repository import ServicioRepository
from datetime import datetime

class ContratoService:
    """Servicio que contiene la lógica de negocio para Contrato"""
    
    @staticmethod
    def get_all_contratos():
        """Obtiene todos los contratos"""
        return ContratoRepository.get_all()
    
    @staticmethod
    def get_contrato_by_id(contrato_id):
        """Obtiene un contrato por ID"""
        return ContratoRepository.get_by_id(contrato_id)
    
    @staticmethod
    def create_contrato(contrato_data):
        """Crea un nuevo contrato con validaciones y lógica de negocio"""
        # Validaciones de negocio
        errors = []
        
        empresa_id = contrato_data.get('empresa_id')
        if not empresa_id:
            errors.append('El ID de empresa es requerido')
        else:
            empresa = EmpresaRepository.get_by_id(empresa_id)
            if not empresa:
                errors.append('La empresa especificada no existe')
        
        servicio_id = contrato_data.get('servicio_id')
        if not servicio_id:
            errors.append('El ID de servicio es requerido')
        else:
            servicio = ServicioRepository.get_by_id(servicio_id)
            if not servicio:
                errors.append('El servicio especificado no existe')
            else:
                # Calcular precio_final basado en precio_base del servicio
                # (puede incluir descuentos, recargos, etc. en el futuro)
                if 'precio_final' not in contrato_data or not contrato_data['precio_final']:
                    contrato_data['precio_final'] = servicio.precio_base
        
        if not contrato_data.get('fecha_inicio'):
            errors.append('La fecha de inicio es requerida')
        else:
            try:
                fecha_inicio = datetime.strptime(contrato_data['fecha_inicio'], '%Y-%m-%d').date()
                if fecha_inicio < datetime.now().date():
                    errors.append('La fecha de inicio no puede ser anterior a hoy')
            except ValueError:
                errors.append('La fecha de inicio debe tener formato YYYY-MM-DD')
        
        if contrato_data.get('fecha_fin'):
            try:
                fecha_fin = datetime.strptime(contrato_data['fecha_fin'], '%Y-%m-%d').date()
                fecha_inicio = datetime.strptime(contrato_data['fecha_inicio'], '%Y-%m-%d').date()
                if fecha_fin < fecha_inicio:
                    errors.append('La fecha de fin debe ser posterior a la fecha de inicio')
            except ValueError:
                errors.append('La fecha de fin debe tener formato YYYY-MM-DD')
        
        precio_final = contrato_data.get('precio_final')
        if precio_final is None:
            errors.append('El precio final es requerido')
        elif precio_final < 0:
            errors.append('El precio final debe ser mayor o igual a 0')
        
        if errors:
            raise ValueError('; '.join(errors))
        
        return ContratoRepository.create(contrato_data)
    
    @staticmethod
    def update_contrato(contrato_id, contrato_data):
        """Actualiza un contrato con validaciones"""
        contrato = ContratoRepository.get_by_id(contrato_id)
        if not contrato:
            raise ValueError('Contrato no encontrado')
        
        # Validaciones de negocio
        if 'empresa_id' in contrato_data:
            empresa = EmpresaRepository.get_by_id(contrato_data['empresa_id'])
            if not empresa:
                raise ValueError('La empresa especificada no existe')
        
        if 'servicio_id' in contrato_data:
            servicio = ServicioRepository.get_by_id(contrato_data['servicio_id'])
            if not servicio:
                raise ValueError('El servicio especificado no existe')
        
        if 'fecha_inicio' in contrato_data and 'fecha_fin' in contrato_data:
            try:
                fecha_inicio = datetime.strptime(contrato_data['fecha_inicio'], '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(contrato_data['fecha_fin'], '%Y-%m-%d').date()
                if fecha_fin < fecha_inicio:
                    raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
            except ValueError as e:
                if 'formato' not in str(e):
                    raise ValueError('Las fechas deben tener formato YYYY-MM-DD')
        
        if 'precio_final' in contrato_data and contrato_data['precio_final'] < 0:
            raise ValueError('El precio final debe ser mayor o igual a 0')
        
        return ContratoRepository.update(contrato_id, contrato_data)
    
    @staticmethod
    def delete_contrato(contrato_id):
        """Elimina un contrato"""
        contrato = ContratoRepository.get_by_id(contrato_id)
        if not contrato:
            raise ValueError('Contrato no encontrado')
        
        return ContratoRepository.delete(contrato_id)



