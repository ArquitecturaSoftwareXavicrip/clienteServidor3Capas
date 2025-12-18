from app.repositories.asignacion_repository import AsignacionRepository
from datetime import datetime

class AsignacionService:
    """Servicio que contiene la lógica de negocio para Asignacion"""
    
    @staticmethod
    def check_overlap(empleado_id, fecha_inicio, fecha_fin, hora_inicio, hora_fin):
        """
        Verifica si hay solapamiento de horario.
        Retorna True si hay solapamiento, False si está libre.
        """
        asignaciones = AsignacionRepository.get_by_empleado_and_date_range(
             empleado_id, fecha_inicio, fecha_fin
        )
        
        for asignacion in asignaciones:
            # Si las fechas coinciden (ya filtrado por Repo), verificar horas
            # Logic: (StartA < EndB) and (EndA > StartB)
            if asignacion.hora_inicio < hora_fin and asignacion.hora_fin > hora_inicio:
                return True
                
        return False

    @staticmethod
    def get_all_asignaciones():
        """Obtiene todas las asignaciones"""
        return AsignacionRepository.get_all()
    
    @staticmethod
    def get_asignacion_by_id(asignacion_id):
        """Obtiene una asignacion por ID"""
        return AsignacionRepository.get_by_id(asignacion_id)
    
    @staticmethod
    def create_asignacion(data):
        """Crea una nueva asignacion con validaciones"""
        errors = []
        
        # Validar campos requeridos
        required_fields = ['contrato_id', 'servicio_id', 'empleado_id', 'espacio_id', 'fecha_inicio', 'hora_inicio', 'hora_fin', 'frecuencia']
        for field in required_fields:
            if field not in data:
                errors.append(f"El campo {field} es requerido")
        
        if errors:
            raise ValueError('; '.join(errors))
            
        # Convertir strings a objetos date/time para comparacion
        try:
            fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date() if data.get('fecha_fin') else None
            hora_inicio = datetime.strptime(data['hora_inicio'], '%H:%M').time()
            hora_fin = datetime.strptime(data['hora_fin'], '%H:%M').time()
            
            # Actualizar data con objetos convertidos
            data['fecha_inicio'] = fecha_inicio
            data['fecha_fin'] = fecha_fin
            data['hora_inicio'] = hora_inicio
            data['hora_fin'] = hora_fin
            
        except ValueError:
            raise ValueError("Formato de fecha (YYYY-MM-DD) u hora (HH:MM) inválido")

        # Validacion de logica: Hora Fin > Hora Inicio
        if hora_inicio >= hora_fin:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")

        # Validacion de solapamiento
        if AsignacionService.check_overlap(data['empleado_id'], fecha_inicio, fecha_fin, hora_inicio, hora_fin):
             raise ValueError("El empleado ya tiene una asignación en ese horario que se solapa")
        
        return AsignacionRepository.create(data)
    
    @staticmethod
    def update_asignacion(asignacion_id, data):
        """Actualiza una asignacion"""
        # Nota: Aquí se deberian repetir validaciones si cambian fechas/horas
        return AsignacionRepository.update(asignacion_id, data)
    
    @staticmethod
    def delete_asignacion(asignacion_id):
        """Elimina una asignacion"""
        return AsignacionRepository.delete(asignacion_id)
