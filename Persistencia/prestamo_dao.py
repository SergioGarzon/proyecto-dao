from Entidades.prestamo import Prestamo
from Persistencia.base_dao import BaseDAO


class PrestamoDAO(BaseDAO):

    def __init__(self, session):
        super().__init__(session, Prestamo)

    def listar_recientes(self):
        return self.session.query(Prestamo).order_by(Prestamo.id_prestamo.desc()).all()
