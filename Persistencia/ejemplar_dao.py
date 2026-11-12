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

    def disponibles_por_libro_y_sede(self, codigo_libro, id_sede):
        return (self.session.query(Ejemplar)
                .filter_by(codigo_libro=codigo_libro, id_sede=id_sede, estado=EstadoEjemplar.DISPONIBLE)
                .order_by(Ejemplar.id_ejemplar)
                .all())

    def contar_por_libro_y_sede(self, codigo_libro, id_sede):
        # Los ejemplares dados de baja no cuentan: nunca van a poder cubrir una reserva
        return (self.session.query(Ejemplar)
                .filter(Ejemplar.codigo_libro == codigo_libro, Ejemplar.id_sede == id_sede,
                        Ejemplar.estado != EstadoEjemplar.BAJA)
                .count())
