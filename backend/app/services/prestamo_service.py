from app.repositories.prestamo_repository import PrestamoRepository

class PrestamoService:
    @staticmethod
    def get_all():
        return PrestamoRepository.get_all()

    @staticmethod
    def get_by_id(id):
        return PrestamoRepository.get_by_id(id)

    @staticmethod
    def create(data):
        if not data.get('equipo'):
            raise ValueError("El nombre del equipo es obligatorio")
        return PrestamoRepository.create(data)

    @staticmethod
    def update(id, data):
        return PrestamoRepository.update(id, data)

    @staticmethod
    def delete(id):
        return PrestamoRepository.delete(id)