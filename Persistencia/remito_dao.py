from Entidades.remito import Remito
from Persistencia.base_dao import BaseDAO


class RemitoDAO(BaseDAO):

    def __init__(self, session):
        super().__init__(session, Remito)

    def siguiente_numero(self, hoy):
        cantidad = self.session.query(Remito).count()
        return f"R-{hoy.year}-{cantidad + 1:05d}"
