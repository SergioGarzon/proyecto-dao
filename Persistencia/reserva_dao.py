from Entidades.enums import EstadoReserva
from Entidades.reserva import Reserva
from Persistencia.base_dao import BaseDAO

VIGENTES = (EstadoReserva.PENDIENTE, EstadoReserva.ASIGNADA)


class ReservaDAO(BaseDAO):

    def __init__(self, session):
        super().__init__(session, Reserva)

    def listar_filtradas(self, estado=None, legajo_dni=None):
        consulta = self.session.query(Reserva)
        if estado is not None:
            consulta = consulta.filter(Reserva.estado == estado)
        if legajo_dni is not None:
            consulta = consulta.filter(Reserva.legajo_dni == legajo_dni)
        return consulta.order_by(Reserva.id_reserva.desc()).all()

    def pendientes_por_libro_y_sede(self, codigo_libro, id_sede):
        # Orden de llegada: la primera reserva pendiente es la primera en recibir un ejemplar
        return (self.session.query(Reserva)
                .filter_by(codigo_libro=codigo_libro, id_sede_retiro=id_sede, estado=EstadoReserva.PENDIENTE)
                .order_by(Reserva.fecha_reserva, Reserva.id_reserva)
                .all())

    def listar_pendientes(self):
        return (self.session.query(Reserva)
                .filter_by(estado=EstadoReserva.PENDIENTE)
                .order_by(Reserva.fecha_reserva, Reserva.id_reserva)
                .all())

    def listar_asignadas_expiradas(self, hoy):
        return (self.session.query(Reserva)
                .filter(Reserva.estado == EstadoReserva.ASIGNADA, Reserva.fecha_expiracion < hoy)
                .order_by(Reserva.id_reserva)
                .all())

    def existe_vigente(self, legajo_dni, codigo_libro):
        return (self.session.query(Reserva.id_reserva)
                .filter(Reserva.legajo_dni == legajo_dni, Reserva.codigo_libro == codigo_libro,
                        Reserva.estado.in_(VIGENTES))
                .first()) is not None

    def contar_vigentes(self, legajo_dni):
        return (self.session.query(Reserva)
                .filter(Reserva.legajo_dni == legajo_dni, Reserva.estado.in_(VIGENTES))
                .count())
