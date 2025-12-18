from app.config.database import db
from app.models.asignacion import Asignacion
from sqlalchemy import and_, or_

class AsignacionRepository:
    """Repositorio para operaciones CRUD de Asignacion"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las asignaciones"""
        return Asignacion.query.all()
    
    @staticmethod
    def get_by_id(asignacion_id):
        """Obtiene una asignacion por su ID"""
        return Asignacion.query.get(asignacion_id)
    
    @staticmethod
    def get_by_empleado_and_date_range(empleado_id, fecha_inicio, fecha_fin):
        """Obtiene asignaciones de un empleado que se solapen con un rango de fechas"""
        query = Asignacion.query.filter(Asignacion.empleado_id == empleado_id)
        
        # Lógica de solapamiento de fechas
        # (StartA <= EndB) and (EndA >= StartB)
        if fecha_fin:
             query = query.filter(
                 or_(
                     Asignacion.fecha_fin == None,
                     and_(
                         Asignacion.fecha_inicio <= fecha_fin,
                         Asignacion.fecha_fin >= fecha_inicio
                     )
                 )
             )
        else:
             # Si la nueva asignación es indefinida, choca con cualquiera que empiece antes o después
             query = query.filter(
                 or_(
                     Asignacion.fecha_fin == None,
                     Asignacion.fecha_fin >= fecha_inicio
                 )
             )
             
        return query.all()

    @staticmethod
    def create(data):
        """Crea una nueva asignacion"""
        asignacion = Asignacion(
            contrato_id=data['contrato_id'],
            servicio_id=data['servicio_id'],
            empleado_id=data['empleado_id'],
            espacio_id=data['espacio_id'],
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data.get('fecha_fin'),
            hora_inicio=data['hora_inicio'],
            hora_fin=data['hora_fin'],
            frecuencia=data['frecuencia'],
            estado=data.get('estado', 'ACTIVO')
        )
        db.session.add(asignacion)
        db.session.commit()
        return asignacion
    
    @staticmethod
    def update(asignacion_id, data):
        """Actualiza una asignacion existente"""
        asignacion = AsignacionRepository.get_by_id(asignacion_id)
        if not asignacion:
            return None
        
        asignacion.contrato_id = data.get('contrato_id', asignacion.contrato_id)
        asignacion.servicio_id = data.get('servicio_id', asignacion.servicio_id)
        asignacion.empleado_id = data.get('empleado_id', asignacion.empleado_id)
        asignacion.espacio_id = data.get('espacio_id', asignacion.espacio_id)
        asignacion.fecha_inicio = data.get('fecha_inicio', asignacion.fecha_inicio)
        asignacion.fecha_fin = data.get('fecha_fin', asignacion.fecha_fin)
        asignacion.hora_inicio = data.get('hora_inicio', asignacion.hora_inicio)
        asignacion.hora_fin = data.get('hora_fin', asignacion.hora_fin)
        asignacion.frecuencia = data.get('frecuencia', asignacion.frecuencia)
        asignacion.estado = data.get('estado', asignacion.estado)
        
        db.session.commit()
        return asignacion
    
    @staticmethod
    def delete(asignacion_id):
        """Elimina una asignacion"""
        asignacion = AsignacionRepository.get_by_id(asignacion_id)
        if not asignacion:
            return False
        
        db.session.delete(asignacion)
        db.session.commit()
        return True
