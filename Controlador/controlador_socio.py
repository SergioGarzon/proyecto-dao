from datetime import date

from Entidades.excepciones import ReglaNegocioError
from Entidades.socio import Socio
from Persistencia.conexion import ConexionBD
from Persistencia.socio_dao import SocioDAO


class ControladorSocio:

    def consultar_socios(self):
        with ConexionBD().obtener_session() as session:
            return [self._a_fila(socio) for socio in SocioDAO(session).listar()]

    def buscar_socio(self, legajo):
        legajo = self._convertir_legajo(legajo)
        with ConexionBD().obtener_session() as session:
            socio = SocioDAO(session).obtener(legajo)
            return [self._a_fila(socio)] if socio else []

    def insertar_socio(self, legajo, nombre, apellido, fecha, domicilio, barrio, localidad):
        legajo = self._convertir_legajo(legajo)
        try:
            fecha_inscripcion = date.fromisoformat(fecha)
        except ValueError:
            raise ReglaNegocioError("La fecha debe tener el formato AAAA-MM-DD.")

        with ConexionBD().obtener_session() as session:
            dao = SocioDAO(session)
            if dao.obtener(legajo) is not None:
                raise ReglaNegocioError("Ya existe un socio con el legajo ingresado.")
            dao.guardar(Socio(legajo_dni=legajo, nombre=nombre, apellido=apellido,
                              fecha_inscripcion=fecha_inscripcion, domicilio_calle=domicilio,
                              barrio=barrio, localidad=localidad))

    def eliminar_socio(self, legajo):
        # Baja lógica: el socio conserva su historial de préstamos y multas
        legajo = self._convertir_legajo(legajo)
        with ConexionBD().obtener_session() as session:
            socio = SocioDAO(session).obtener(legajo)
            if socio is None:
                raise ReglaNegocioError(f"No se encontró un socio con legajo {legajo}.")
            socio.dar_baja()

    def _convertir_legajo(self, legajo):
        try:
            return int(legajo)
        except ValueError:
            raise ReglaNegocioError("El legajo debe ser un número.")

    def _a_fila(self, socio):
        return (socio.legajo_dni, socio.nombre, socio.apellido, socio.fecha_inscripcion, socio.domicilio_calle,
                socio.barrio, socio.localidad, socio.estado.value)
