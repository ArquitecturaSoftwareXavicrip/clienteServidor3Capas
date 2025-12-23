"""
Servicio de Permiso - Tier 2: Lógica de Negocio
Contiene la lógica de negocio y validaciones para Permiso
"""
from datetime import datetime
from app.repositories.permiso_repository import PermisoRepository

class PermisoService:
    """Servicio que contiene la lógica de negocio para Permiso"""
    
    @staticmethod
    def get_all_permisos():
        """Obtiene todos los permisos"""
        return PermisoRepository.get_all()
    
    @staticmethod
    def get_permiso_by_id(permiso_id):
        """Obtiene un permiso por ID"""
        return PermisoRepository.get_by_id(permiso_id)
    
    @staticmethod
    def get_permisos_by_estado(estado):
        """Obtiene permisos por estado"""
        estados_validos = ['pendiente', 'aprobado', 'rechazado']
        if estado not in estados_validos:
            raise ValueError(f'Estado inválido. Debe ser uno de: {", ".join(estados_validos)}')
        return PermisoRepository.get_by_estado(estado)
    
    @staticmethod
    def create_permiso(permiso_data):
        """Crea un nuevo permiso con validaciones"""
        # Validaciones de negocio
        errors = []
        
        if not permiso_data.get('empleado') or len(permiso_data['empleado'].strip()) == 0:
            errors.append('El nombre del empleado es requerido')
        
        if not permiso_data.get('fecha_inicio'):
            errors.append('La fecha de inicio es requerida')
        
        if not permiso_data.get('fecha_fin'):
            errors.append('La fecha de fin es requerida')
        
        if not permiso_data.get('dias_solicitados'):
            errors.append('Los días solicitados son requeridos')
        elif permiso_data['dias_solicitados'] <= 0:
            errors.append('Los días solicitados deben ser mayor a 0')
        
        # Validar formato de fechas y convertir strings a objetos date
        try:
            if isinstance(permiso_data.get('fecha_inicio'), str):
                fecha_inicio = datetime.strptime(permiso_data['fecha_inicio'], '%Y-%m-%d').date()
                permiso_data['fecha_inicio'] = fecha_inicio
            else:
                fecha_inicio = permiso_data.get('fecha_inicio')
        except (ValueError, TypeError):
            errors.append('Formato de fecha de inicio inválido. Use YYYY-MM-DD')
            fecha_inicio = None
        
        try:
            if isinstance(permiso_data.get('fecha_fin'), str):
                fecha_fin = datetime.strptime(permiso_data['fecha_fin'], '%Y-%m-%d').date()
                permiso_data['fecha_fin'] = fecha_fin
            else:
                fecha_fin = permiso_data.get('fecha_fin')
        except (ValueError, TypeError):
            errors.append('Formato de fecha de fin inválido. Use YYYY-MM-DD')
            fecha_fin = None
        
        # Validar que fecha_fin sea mayor a fecha_inicio
        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                errors.append('La fecha de fin debe ser posterior a la fecha de inicio')
            
            # Validar que los días solicitados sean coherentes con el rango de fechas
            dias_reales = (fecha_fin - fecha_inicio).days
            if permiso_data.get('dias_solicitados') and permiso_data['dias_solicitados'] > dias_reales:
                errors.append(f'Los días solicitados ({permiso_data["dias_solicitados"]}) no pueden ser mayores al rango de fechas ({dias_reales} días)')
        
        # Validar estado si se proporciona
        if permiso_data.get('estado'):
            estados_validos = ['pendiente', 'aprobado', 'rechazado']
            if permiso_data['estado'] not in estados_validos:
                errors.append(f'Estado inválido. Debe ser uno de: {", ".join(estados_validos)}')
        
        if errors:
            raise ValueError('; '.join(errors))
        
        return PermisoRepository.create(permiso_data)
    
    @staticmethod
    def update_permiso(permiso_id, permiso_data):
        """Actualiza un permiso con validaciones"""
        permiso = PermisoRepository.get_by_id(permiso_id)
        if not permiso:
            raise ValueError('Permiso no encontrado')
        
        # Validaciones de negocio
        if 'dias_solicitados' in permiso_data:
            if permiso_data['dias_solicitados'] <= 0:
                raise ValueError('Los días solicitados deben ser mayor a 0')
        
        # Validar y convertir fechas si se proporcionan
        if 'fecha_inicio' in permiso_data and isinstance(permiso_data['fecha_inicio'], str):
            try:
                permiso_data['fecha_inicio'] = datetime.strptime(permiso_data['fecha_inicio'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                raise ValueError('Formato de fecha de inicio inválido. Use YYYY-MM-DD')
        
        if 'fecha_fin' in permiso_data and isinstance(permiso_data['fecha_fin'], str):
            try:
                permiso_data['fecha_fin'] = datetime.strptime(permiso_data['fecha_fin'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                raise ValueError('Formato de fecha de fin inválido. Use YYYY-MM-DD')
        
        # Validar estado si se proporciona
        if 'estado' in permiso_data:
            estados_validos = ['pendiente', 'aprobado', 'rechazado']
            if permiso_data['estado'] not in estados_validos:
                raise ValueError(f'Estado inválido. Debe ser uno de: {", ".join(estados_validos)}')
        
        return PermisoRepository.update(permiso_id, permiso_data)
    
    @staticmethod
    def delete_permiso(permiso_id):
        """Elimina un permiso"""
        permiso = PermisoRepository.get_by_id(permiso_id)
        if not permiso:
            raise ValueError('Permiso no encontrado')
        
        return PermisoRepository.delete(permiso_id)
    
    @staticmethod
    def aprobar_permiso(permiso_id, observaciones=None):
        """Aprueba un permiso"""
        permiso = PermisoRepository.get_by_id(permiso_id)
        if not permiso:
            raise ValueError('Permiso no encontrado')
        
        update_data = {'estado': 'aprobado'}
        if observaciones:
            update_data['observaciones'] = observaciones
        
        return PermisoRepository.update(permiso_id, update_data)
    
    @staticmethod
    def rechazar_permiso(permiso_id, observaciones=None):
        """Rechaza un permiso"""
        permiso = PermisoRepository.get_by_id(permiso_id)
        if not permiso:
            raise ValueError('Permiso no encontrado')
        
        update_data = {'estado': 'rechazado'}
        if observaciones:
            update_data['observaciones'] = observaciones
        
        return PermisoRepository.update(permiso_id, update_data)

