"""
Repositorio de Permiso - Tier 3: Acceso a Datos
Encapsula todas las operaciones de acceso a datos para Permiso
"""
from app.config.database import db
from app.models.permiso import Permiso

class PermisoRepository:
    """Repositorio para operaciones CRUD de Permiso"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los permisos"""
        return Permiso.query.all()
    
    @staticmethod
    def get_by_id(permiso_id):
        """Obtiene un permiso por su ID"""
        return Permiso.query.get(permiso_id)
    
    @staticmethod
    def get_by_estado(estado):
        """Obtiene permisos por estado (pendiente, aprobado, rechazado)"""
        return Permiso.query.filter_by(estado=estado).all()
    
    @staticmethod
    def create(permiso_data):
        """Crea un nuevo permiso"""
        permiso = Permiso(
            empleado=permiso_data['empleado'],
            tipo=permiso_data.get('tipo', 'Vacaciones'),
            fecha_inicio=permiso_data['fecha_inicio'],
            fecha_fin=permiso_data['fecha_fin'],
            dias_solicitados=permiso_data['dias_solicitados'],
            estado=permiso_data.get('estado', 'pendiente'),
            observaciones=permiso_data.get('observaciones', '')
        )
        db.session.add(permiso)
        db.session.commit()
        return permiso
    
    @staticmethod
    def update(permiso_id, permiso_data):
        """Actualiza un permiso existente"""
        permiso = PermisoRepository.get_by_id(permiso_id)
        if not permiso:
            return None
        
        permiso.empleado = permiso_data.get('empleado', permiso.empleado)
        permiso.tipo = permiso_data.get('tipo', permiso.tipo)
        permiso.fecha_inicio = permiso_data.get('fecha_inicio', permiso.fecha_inicio)
        permiso.fecha_fin = permiso_data.get('fecha_fin', permiso.fecha_fin)
        permiso.dias_solicitados = permiso_data.get('dias_solicitados', permiso.dias_solicitados)
        permiso.estado = permiso_data.get('estado', permiso.estado)
        permiso.observaciones = permiso_data.get('observaciones', permiso.observaciones)
        
        db.session.commit()
        return permiso
    
    @staticmethod
    def delete(permiso_id):
        """Elimina un permiso"""
        permiso = PermisoRepository.get_by_id(permiso_id)
        if not permiso:
            return False
        
        db.session.delete(permiso)
        db.session.commit()
        return True

