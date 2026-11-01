from Entidades.enums import EstadoSocio
from Entidades.socio import Socio
from Persistencia.base_dao import BaseDAO


class SocioDAO(BaseDAO):

    def __init__(self, session):
        super().__init__(session, Socio)

    def listar_habilitados(self):
        return (self.session.query(Socio)
                .filter_by(estado=EstadoSocio.ACTIVO)
                .order_by(Socio.apellido)
                .all())
