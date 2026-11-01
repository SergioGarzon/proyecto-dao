from Entidades.ejemplar import Ejemplar
from Entidades.enums import EstadoEjemplar
from Persistencia.base_dao import BaseDAO


class EjemplarDAO(BaseDAO):

    def __init__(self, session):
        super().__init__(session, Ejemplar)

    def disponibles_por_sede(self, id_sede):
        return (self.session.query(Ejemplar)
                .filter_by(id_sede=id_sede, estado=EstadoEjemplar.DISPONIBLE)
                .order_by(Ejemplar.id_ejemplar)
                .all())
