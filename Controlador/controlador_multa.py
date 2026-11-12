from datetime import date

from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import ConexionBD
from Persistencia.multa_dao import MultaDAO
from Persistencia.socio_dao import SocioDAO


class ControladorMulta:

    # Opciones del filtro de estado: texto del combo -> valor para el DAO
    ESTADOS = ("Todas", "Pendientes", "Pagadas")
    _FILTRO_PENDIENTES = {"Todas": None, "Pendientes": True, "Pagadas": False}

    # Consultas para cargar la pantalla
    def consultar_multas(self, estado="Todas", legajo=None):
        if estado not in self._FILTRO_PENDIENTES:
            raise ReglaNegocioError("Debe elegir un estado válido.")
        legajo = self._convertir_entero(legajo, "El legajo") if legajo not in (None, "") else None
        with ConexionBD().obtener_session() as session:
            multas = MultaDAO(session).listar_filtradas(self._FILTRO_PENDIENTES[estado], legajo)
            return [self._a_fila(multa) for multa in multas]

    def consultar_deuda(self, legajo):
        with ConexionBD().obtener_session() as session:
            socio = self._obtener_socio(session, legajo)
            pendientes = [multa for multa in socio.multas if multa.esta_pendiente()]
            return f"{socio.apellido}, {socio.nombre}", len(pendientes), socio.total_multas_pendientes()

    # Casos de uso
    def pagar_multas(self, ids_multa, hoy=None):
        """Registra el pago de las multas elegidas. Si alguna no se puede pagar, no se paga ninguna."""
        hoy = hoy or date.today()
        if not ids_multa:
            raise ReglaNegocioError("Debe seleccionar una o más multas para registrar el pago.")

        with ConexionBD().obtener_session() as session:
            dao = MultaDAO(session)
            total = 0
            socios = set()
            for id_multa in ids_multa:
                id_multa = self._convertir_entero(id_multa, "El número de multa")
                multa = dao.obtener(id_multa)
                if multa is None:
                    raise ReglaNegocioError(f"No se encontró la multa {id_multa}.")
                multa.pagar(hoy)
                total += multa.monto
                socios.add(multa.socio)
            # Si ya no le queda deuda, el socio vuelve a estar habilitado
            for socio in socios:
                socio.actualizar_habilitacion(hoy)
            return total

    def pagar_todas_del_socio(self, legajo, hoy=None):
        hoy = hoy or date.today()
        with ConexionBD().obtener_session() as session:
            socio = self._obtener_socio(session, legajo)
            pendientes = MultaDAO(session).pendientes_de_socio(socio.legajo_dni)
            if not pendientes:
                raise ReglaNegocioError(f"El socio {socio.legajo_dni} no tiene multas pendientes.")
            for multa in pendientes:
                multa.pagar(hoy)
            socio.actualizar_habilitacion(hoy)
            return len(pendientes), sum(multa.monto for multa in pendientes)

    # Auxiliares
    def _obtener_socio(self, session, legajo):
        legajo = self._convertir_entero(legajo, "El legajo")
        socio = SocioDAO(session).obtener(legajo)
        if socio is None:
            raise ReglaNegocioError(f"No se encontró un socio con legajo {legajo}.")
        return socio

    def _convertir_entero(self, valor, campo):
        try:
            return int(valor)
        except (TypeError, ValueError):
            raise ReglaNegocioError(f"{campo} debe ser un número.")

    def _a_fila(self, multa):
        socio = multa.socio
        detalle = multa.detalle
        return (multa.id_multa, f"{socio.legajo_dni} - {socio.apellido}, {socio.nombre}", multa.motivo.value,
                detalle.ejemplar.libro.titulo, detalle.id_prestamo, multa.monto, multa.fecha_generacion,
                multa.fecha_pago or "-", multa.estado_texto())
