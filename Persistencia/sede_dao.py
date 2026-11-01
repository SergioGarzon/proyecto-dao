from Entidades.enums import EstadoSede
from Entidades.sede import Sede
from Persistencia.base_dao import BaseDAO


class SedeDAO(BaseDAO):

    def __init__(self, session):
        super().__init__(session, Sede)

    def listar_activas(self):
        return (self.session.query(Sede)
                .filter_by(estado=EstadoSede.ACTIVA)
                .order_by(Sede.id_sede)
                .all())
