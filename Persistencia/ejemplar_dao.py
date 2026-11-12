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
    
    def listar_por_libro(self, codigo_libro):
        return (self.session.query(Ejemplar)
                .filter_by(codigo_libro=codigo_libro)
                .order_by(Ejemplar.id_ejemplar)
                .all())

    def buscar_por_codigo(self, codigo_inventario):
        return (self.session.query(Ejemplar)
                .filter_by(codigo_inventario=codigo_inventario)
                .first())
    
