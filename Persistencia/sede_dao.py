"""Consultas de sedes. Reutiliza BaseDAO y la sesión del controlador."""
from sqlalchemy import func, or_

from Entidades.enums import EstadoPrestamo, EstadoReserva, EstadoSede
from Entidades.prestamo import Prestamo
from Entidades.remito import Remito
from Entidades.reserva import Reserva
from Entidades.estado_remito import ESTADOS_ABIERTOS
from Entidades.sede import Sede
from Persistencia.base_dao import BaseDAO


class SedeDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session, Sede)

    def listar_activas(self):
        # Este método ya existía y es utilizado por ControladorPrestamo.
        return (self.session.query(Sede)
                .filter_by(estado=EstadoSede.ACTIVA)
                .order_by(Sede.id_sede)
                .all())

    def listar_ordenadas(self):
        return self.session.query(Sede).order_by(Sede.id_sede).all()

    def buscar(self, texto):
        """Por ID exacto cuando es numérico, o por parte del nombre."""
        termino = texto.strip()
        if not termino:
            return self.listar_ordenadas()
        if termino.isdecimal():
            sede = self.obtener(int(termino))
            return [sede] if sede is not None else []
        # Escapamos caracteres de LIKE para que % y _ sean texto literal.
        termino = termino.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        return (self.session.query(Sede)
                .filter(Sede.nombre.ilike(f'%{termino}%', escape='\\'))
                .order_by(Sede.id_sede)
                .all())

    def existe_nombre(self, nombre, excluir_id=None):
        consulta = self.session.query(Sede.id_sede).filter(
            func.lower(func.trim(Sede.nombre)) == nombre.strip().lower()
        )
        if excluir_id is not None:
            consulta = consulta.filter(Sede.id_sede != excluir_id)
        return consulta.first() is not None

    def motivo_baja_bloqueada(self, id_sede):
        """No interrumpimos operaciones que dependen de que la sede siga activa.

        Es una protección adicional del equipo; la consigna exige no INICIAR
        operaciones con sedes de baja, pero no define cómo cerrar una sede con
        operaciones pendientes.
        """
        prestamos = (self.session.query(Prestamo.id_prestamo)
                     .filter(or_(Prestamo.id_sede_origen == id_sede,
                                 Prestamo.id_sede_destino == id_sede),
                             # Devuelto, con incidencia y cancelado son estados finales
                             Prestamo.estado.in_((EstadoPrestamo.PENDIENTE_ENVIO,
                                                  EstadoPrestamo.ACTIVO)))
                     .first())
        if prestamos:
            return 'Tiene préstamos sin cerrar (pendientes de envío o activos).'

        remitos = (self.session.query(Remito.id_remito)
                   .filter(or_(Remito.id_sede_origen == id_sede,
                               Remito.id_sede_destino == id_sede),
                           Remito.estado.in_(ESTADOS_ABIERTOS))
                   .first())
        if remitos:
            return 'Tiene remitos pendientes de completar.'

        reservas = (self.session.query(Reserva.id_reserva)
                    .filter(Reserva.id_sede_retiro == id_sede,
                            Reserva.estado.in_((EstadoReserva.PENDIENTE,
                                                EstadoReserva.ASIGNADA)))
                    .first())
        if reservas:
            return 'Tiene reservas vigentes.'
        return None
