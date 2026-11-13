from datetime import date

from Controlador.controlador_reserva import ControladorReserva
from Entidades.excepciones import ReglaNegocioError
from Entidades.remito import Remito
from Persistencia.conexion import ConexionBD
from Persistencia.remito_dao import RemitoDAO


class ControladorRemito:
    # Consultas para cargar las pantallas
    def consultar_remitos(self, estado=None):
        with ConexionBD().obtener_session() as session:
            return [(remito.id_remito, remito.numero, remito.tipo.value, remito.id_prestamo,
                     str(remito.sede_origen), str(remito.sede_destino), remito.fecha_emision,
                     remito.estado, ", ".join(ejemplar.codigo_inventario for ejemplar in remito.ejemplares))
                    for remito in RemitoDAO(session).listar_por_estado(estado)]

    def consultar_historial(self, id_remito):
        with ConexionBD().obtener_session() as session:
            remito = self._obtener(session, id_remito)
            return [(fila.fecha_hora, fila.estado_anterior or "-", fila.estado_nuevo, fila.observacion or "")
                    for fila in remito.historial]

    # Ciclo de vida del remito: el State decide si cada transición es válida
    def despachar(self, id_remito, observacion=""):
        self._avanzar(id_remito, Remito.despachar, observacion)

    def iniciar_transito(self, id_remito, observacion=""):
        self._avanzar(id_remito, Remito.iniciar_transito, observacion)

    def recibir(self, id_remito, observacion=""):
        self._avanzar(id_remito, Remito.recibir, observacion)

    def reportar_danio(self, id_remito, observacion=""):
        self._avanzar(id_remito, Remito.reportar_danio, observacion)

    def reportar_extravio(self, id_remito, observacion=""):
        self._avanzar(id_remito, Remito.reportar_extravio, observacion)

    def cancelar(self, id_remito, observacion="", hoy=None):
        """Cancela un envío que todavía no salió: el préstamo queda cancelado y los ejemplares disponibles."""
        hoy = hoy or date.today()
        with ConexionBD().obtener_session() as session:
            remito = self._avanzar_en_sesion(session, id_remito, Remito.cancelar, observacion)
            # Los ejemplares liberados pasan a las reservas que los estaban esperando
            reservas = ControladorReserva()
            for codigo_libro, id_sede in sorted({(ejemplar.codigo_libro, ejemplar.id_sede)
                                                 for ejemplar in remito.ejemplares}):
                reservas.asignar_pendientes(session, codigo_libro, id_sede, hoy)

    def _avanzar(self, id_remito, operacion, observacion):
        # Toda la operación usa una sesión: si el State rechaza la transición, no se guarda nada
        with ConexionBD().obtener_session() as session:
            self._avanzar_en_sesion(session, id_remito, operacion, observacion)

    def _avanzar_en_sesion(self, session, id_remito, operacion, observacion):
        remito = self._obtener(session, id_remito)
        operacion(remito)
        if observacion.strip():
            remito.historial[-1].observacion = observacion.strip()[:200]
        return remito

    def _obtener(self, session, id_remito):
        remito = RemitoDAO(session).obtener(id_remito)
        if remito is None:
            raise ReglaNegocioError(f"No se encontró un remito con id {id_remito}.")
        return remito