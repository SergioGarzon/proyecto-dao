from datetime import date

from Controlador.controlador_prestamo import ControladorPrestamo
from Entidades.enums import EstadoReserva, TipoPrestamo
from Entidades.excepciones import ReglaNegocioError
from Entidades.reserva import Reserva
from Persistencia.conexion import ConexionBD
from Persistencia.ejemplar_dao import EjemplarDAO
from Persistencia.libro_dao import LibroDAO
from Persistencia.reserva_dao import ReservaDAO
from Persistencia.sede_dao import SedeDAO
from Persistencia.socio_dao import SocioDAO


class ControladorReserva:

    # Consultas para cargar las pantallas
    def consultar_reservas(self, estado=None, legajo=None):
        estado = EstadoReserva(estado) if estado else None
        legajo = self._convertir_entero(legajo, "El legajo") if legajo not in (None, "") else None
        with ConexionBD().obtener_session() as session:
            return [self._a_fila(reserva) for reserva in ReservaDAO(session).listar_filtradas(estado, legajo)]

    def consultar_disponibilidad(self, codigo_libro, id_sede):
        with ConexionBD().obtener_session() as session:
            return len(EjemplarDAO(session).disponibles_por_libro_y_sede(int(codigo_libro), int(id_sede)))

    # Casos de uso
    def crear_reserva(self, legajo, codigo_libro, id_sede, hoy=None):
        hoy = hoy or date.today()
        legajo = self._convertir_entero(legajo, "El legajo")
        codigo_libro = self._convertir_entero(codigo_libro, "El libro")
        id_sede = self._convertir_entero(id_sede, "La sede")

        with ConexionBD().obtener_session() as session:
            socio = SocioDAO(session).obtener(legajo)
            if socio is None:
                raise ReglaNegocioError(f"No se encontró un socio con legajo {legajo}.")
            socio.validar_habilitado(hoy)

            sede = SedeDAO(session).obtener(id_sede)
            if sede is None:
                raise ReglaNegocioError(f"No se encontró la sede {id_sede}.")
            sede.validar_activa()

            libro = LibroDAO(session).obtener(codigo_libro)
            if libro is None:
                raise ReglaNegocioError(f"No se encontró el libro {codigo_libro}.")
            if EjemplarDAO(session).contar_por_libro_y_sede(codigo_libro, id_sede) == 0:
                raise ReglaNegocioError(f"La sede {sede.nombre} no tiene ejemplares de \"{libro.titulo}\".")

            reserva_dao = ReservaDAO(session)
            if reserva_dao.existe_vigente(legajo, codigo_libro):
                raise ReglaNegocioError(f"El socio {legajo} ya tiene una reserva vigente de \"{libro.titulo}\".")
            if reserva_dao.contar_vigentes(legajo) >= Reserva.MAX_RESERVAS_VIGENTES:
                raise ReglaNegocioError(
                    f"El socio {legajo} ya tiene {Reserva.MAX_RESERVAS_VIGENTES} reservas vigentes, que es el máximo.")

            reserva = Reserva(socio=socio, libro=libro, sede_retiro=sede, fecha_reserva=hoy,
                              estado=EstadoReserva.PENDIENTE)
            reserva_dao.guardar(reserva)
            # Si hay un ejemplar libre, la reserva nueva lo toma enseguida (es la última en la fila)
            self.asignar_pendientes(session, codigo_libro, id_sede, hoy)
            session.flush()
            return reserva.id_reserva, reserva.estado.value

    def cancelar_reserva(self, id_reserva, hoy=None):
        hoy = hoy or date.today()
        with ConexionBD().obtener_session() as session:
            reserva = self._obtener(session, id_reserva)
            tenia_ejemplar = reserva.estado == EstadoReserva.ASIGNADA
            reserva.cancelar()
            if tenia_ejemplar:
                # El ejemplar liberado pasa al siguiente socio que lo estaba esperando
                self.asignar_pendientes(session, reserva.codigo_libro, reserva.id_sede_retiro, hoy)

    def cumplir_reserva(self, id_reserva, hoy=None):
        """El socio retira el ejemplar: la reserva se cumple y se registra un préstamo local."""
        hoy = hoy or date.today()
        with ConexionBD().obtener_session() as session:
            reserva = self._obtener(session, id_reserva)
            if not reserva.esta_expirada(hoy):
                id_ejemplar = reserva.id_ejemplar
                reserva.cumplir(hoy)  # Libera el ejemplar para que el préstamo lo pueda tomar
                # Misma sesión: si el préstamo no se puede registrar, la reserva sigue asignada
                return ControladorPrestamo().crear_prestamo_en_sesion(
                    session, reserva.legajo_dni, reserva.id_sede_retiro, reserva.id_sede_retiro,
                    TipoPrestamo.LOCAL.value, [id_ejemplar], hoy)

            # Venció: se guarda el vencimiento (y la reasignación) antes de avisar el error
            fecha_expiracion = reserva.fecha_expiracion
            self._vencer(session, reserva, hoy)
        raise ReglaNegocioError(f"La reserva {id_reserva} venció el {fecha_expiracion:%d/%m/%Y} y ya no se puede retirar.")

    def procesar_reservas(self, hoy=None):
        """Vence las reservas asignadas que no se retiraron y asigna ejemplares a las pendientes."""
        hoy = hoy or date.today()
        with ConexionBD().obtener_session() as session:
            reserva_dao = ReservaDAO(session)
            vencidas = reserva_dao.listar_asignadas_expiradas(hoy)
            for reserva in vencidas:
                reserva.vencer(hoy)

            asignadas = 0
            grupos = {(reserva.codigo_libro, reserva.id_sede_retiro) for reserva in reserva_dao.listar_pendientes()}
            for codigo_libro, id_sede in sorted(grupos):
                asignadas += self.asignar_pendientes(session, codigo_libro, id_sede, hoy)
            return len(vencidas), asignadas

    # Auxiliares
    def _vencer(self, session, reserva, hoy):
        reserva.vencer(hoy)
        self.asignar_pendientes(session, reserva.codigo_libro, reserva.id_sede_retiro, hoy)

    def asignar_pendientes(self, session, codigo_libro, id_sede, hoy):
        # Orden de llegada: cada ejemplar disponible va a la reserva pendiente más antigua
        pendientes = ReservaDAO(session).pendientes_por_libro_y_sede(codigo_libro, id_sede)
        disponibles = EjemplarDAO(session).disponibles_por_libro_y_sede(codigo_libro, id_sede)
        asignadas = 0
        for reserva, ejemplar in zip(pendientes, disponibles):
            reserva.asignar_ejemplar(ejemplar, hoy)
            asignadas += 1
        return asignadas

    def _obtener(self, session, id_reserva):
        id_reserva = self._convertir_entero(id_reserva, "El número de reserva")
        reserva = ReservaDAO(session).obtener(id_reserva)
        if reserva is None:
            raise ReglaNegocioError(f"No se encontró la reserva {id_reserva}.")
        return reserva

    def _convertir_entero(self, valor, campo):
        try:
            return int(valor)
        except (TypeError, ValueError):
            raise ReglaNegocioError(f"{campo} debe ser un número.")

    def _a_fila(self, reserva):
        socio = reserva.socio
        return (reserva.id_reserva, reserva.legajo_dni, f"{socio.apellido}, {socio.nombre}", reserva.libro.titulo,
                reserva.sede_retiro.nombre, reserva.fecha_reserva,
                reserva.ejemplar.codigo_inventario if reserva.ejemplar else "-",
                reserva.fecha_expiracion or "-", reserva.estado.value)
