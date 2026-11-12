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

    def obtener_socio(self, legajo):
        # Datos para precargar el formulario de edición
        with ConexionBD().obtener_session() as session:
            socio = self._obtener_o_error(SocioDAO(session), legajo)
            return {
                "legajo": socio.legajo_dni,
                "nombre": socio.nombre,
                "apellido": socio.apellido,
                "fecha": socio.fecha_inscripcion.isoformat(),
                "domicilio": socio.domicilio_calle,
                "barrio": socio.barrio,
                "localidad": socio.localidad,
            }

    def insertar_socio(self, legajo, nombre, apellido, fecha, domicilio, barrio, localidad):
        legajo = self._convertir_legajo(legajo)
        datos = self._validar_datos(nombre, apellido, fecha, domicilio, barrio, localidad)

        with ConexionBD().obtener_session() as session:
            dao = SocioDAO(session)
            if dao.obtener(legajo) is not None:
                raise ReglaNegocioError("Ya existe un socio con el legajo ingresado.")
            dao.guardar(Socio(legajo_dni=legajo, **datos))

    def modificar_socio(self, legajo, nombre, apellido, fecha, domicilio, barrio, localidad):
        # El legajo no se modifica: es la clave primaria del socio
        datos = self._validar_datos(nombre, apellido, fecha, domicilio, barrio, localidad)

        with ConexionBD().obtener_session() as session:
            socio = self._obtener_o_error(SocioDAO(session), legajo)
            for atributo, valor in datos.items():
                setattr(socio, atributo, valor)

    def habilitar_socio(self, legajo):
        with ConexionBD().obtener_session() as session:
            self._obtener_o_error(SocioDAO(session), legajo).habilitar()

    def inhabilitar_socio(self, legajo):
        with ConexionBD().obtener_session() as session:
            self._obtener_o_error(SocioDAO(session), legajo).inhabilitar()

    def eliminar_socio(self, legajo):
        # Baja lógica: el socio conserva su historial de préstamos y multas
        with ConexionBD().obtener_session() as session:
            self._obtener_o_error(SocioDAO(session), legajo).dar_baja()

    def _obtener_o_error(self, dao, legajo):
        legajo = self._convertir_legajo(legajo)
        socio = dao.obtener(legajo)
        if socio is None:
            raise ReglaNegocioError(f"No se encontró un socio con legajo {legajo}.")
        return socio

    def _validar_datos(self, nombre, apellido, fecha, domicilio, barrio, localidad):
        valores = {
            "nombre": (nombre or "").strip(),
            "apellido": (apellido or "").strip(),
            "domicilio_calle": (domicilio or "").strip(),
            "barrio": (barrio or "").strip(),
            "localidad": (localidad or "").strip(),
        }
        etiquetas = {"nombre": "Nombre", "apellido": "Apellido", "domicilio_calle": "Domicilio",
                     "barrio": "Barrio", "localidad": "Localidad"}
        largos = {"nombre": 60, "apellido": 60, "domicilio_calle": 100, "barrio": 60, "localidad": 60}

        for campo, valor in valores.items():
            if not valor:
                raise ReglaNegocioError(f"El campo {etiquetas[campo]} es obligatorio.")
            if len(valor) > largos[campo]:
                raise ReglaNegocioError(f"{etiquetas[campo]} admite hasta {largos[campo]} caracteres.")

        try:
            fecha_inscripcion = date.fromisoformat((fecha or "").strip())
        except ValueError:
            raise ReglaNegocioError("La fecha debe tener el formato AAAA-MM-DD.")
        if fecha_inscripcion > date.today():
            raise ReglaNegocioError("La fecha de inscripción no puede ser futura.")

        valores["fecha_inscripcion"] = fecha_inscripcion
        return valores

    def _convertir_legajo(self, legajo):
        try:
            return int(legajo)
        except (TypeError, ValueError):
            raise ReglaNegocioError("El legajo debe ser un número.")

    def _a_fila(self, socio):
        return (socio.legajo_dni, socio.nombre, socio.apellido, socio.fecha_inscripcion, socio.domicilio_calle,
                socio.barrio, socio.localidad, socio.estado.value)
