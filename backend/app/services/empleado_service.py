from app.repositories.empleado_repository import EmpleadoRepository


class EmpleadoService:
    """Servicio que contiene la lógica de negocio para Empleado"""

    @staticmethod
    def get_all_empleados():
        return EmpleadoRepository.get_all()

    @staticmethod
    def get_empleado_by_id(empleado_id):
        return EmpleadoRepository.get_by_id(empleado_id)

    @staticmethod
    def create_empleado(empleado_data):
        errors = []
        if not empleado_data.get('nombre') or len(empleado_data['nombre'].strip()) == 0:
            errors.append('El nombre es requerido')
        if not empleado_data.get('apellido') or len(empleado_data['apellido'].strip()) == 0:
            errors.append('El apellido es requerido')
        if not empleado_data.get('email') or '@' not in empleado_data.get('email', ''):
            errors.append('Email inválido')
        if not empleado_data.get('telefono'):
            errors.append('Teléfono es requerido')
        if not empleado_data.get('cargo'):
            errors.append('Cargo es requerido')

        if errors:
            raise ValueError('; '.join(errors))

        return EmpleadoRepository.create(empleado_data)

    @staticmethod
    def update_empleado(empleado_id, empleado_data):
        empleado = EmpleadoRepository.get_by_id(empleado_id)
        if not empleado:
            raise ValueError('Empleado no encontrado')

        if 'email' in empleado_data and empleado_data['email'] and '@' not in empleado_data['email']:
            raise ValueError('Email inválido')

        return EmpleadoRepository.update(empleado_id, empleado_data)

    @staticmethod
    def delete_empleado(empleado_id):
        empleado = EmpleadoRepository.get_by_id(empleado_id)
        if not empleado:
            raise ValueError('Empleado no encontrado')
        return EmpleadoRepository.delete(empleado_id)
