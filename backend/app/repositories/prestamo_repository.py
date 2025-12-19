from app.config.database import db
from app.models.prestamo import Prestamo

class PrestamoRepository:
    @staticmethod
    def get_all():
        return Prestamo.query.all()

    @staticmethod
    def get_by_id(id):
        return Prestamo.query.get(id)

    @staticmethod
    def create(data):
        nuevo_p = Prestamo(equipo=data['equipo'], fecha_prestamo=data['fecha_prestamo'])
        db.session.add(nuevo_p)
        db.session.commit()
        return nuevo_p

    @staticmethod
    def update(id, data):
        p = Prestamo.query.get(id)
        if p:
            p.equipo = data.get('equipo', p.equipo)
            p.fecha_prestamo = data.get('fecha_prestamo', p.fecha_prestamo)
            db.session.commit()
        return p

    @staticmethod
    def delete(id):
        p = Prestamo.query.get(id)
        if p:
            db.session.delete(p)
            db.session.commit()
            return True
        return False