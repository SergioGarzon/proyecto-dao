"""Casos de uso para administrar sedes, con reglas de negocio y sesiones cortas."""
import re
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from Entidades.enums import EstadoSede
from Entidades.excepciones import ReglaNegocioError
from Entidades.sede import Sede
from Persistencia.conexion import ConexionBD
from Persistencia.sede_dao import SedeDAO


class ControladorSede:
    def consultar_sedes(self):
        with ConexionBD().obtener_session() as session:
            return [self._a_fila(sede) for sede in SedeDAO(session).listar_ordenadas()]

    def buscar_sede(self, texto):
        with ConexionBD().obtener_session() as session:
            return [self._a_fila(sede) for sede in SedeDAO(session).buscar(texto)]

    def obtener_sede(self, id_sede):
        with ConexionBD().obtener_session() as session:
            sede = self._obtener_o_error(SedeDAO(session), id_sede)
            return self._a_datos(sede)

    def insertar_sede(self, nombre, direccion, barrio, localidad, telefono, email,
                      hora_apertura, hora_cierre):
        datos = self._validar_datos(nombre, direccion, barrio, localidad,
                                   telefono, email, hora_apertura, hora_cierre)
        try:
            with ConexionBD().obtener_session() as session:
                dao = SedeDAO(session)
                if dao.existe_nombre(datos['nombre']):
                    raise ReglaNegocioError('Ya existe una sede con ese nombre.')
                sede = Sede(**datos, estado=EstadoSede.ACTIVA)
                dao.guardar(sede)
                session.flush()
                return sede.id_sede
        except IntegrityError as error:
            raise ReglaNegocioError('No se pudo crear: ya existe una sede con esos datos.') from error

    def modificar_sede(self, id_sede, nombre, direccion, barrio, localidad,
                       telefono, email, hora_apertura, hora_cierre):
        datos = self._validar_datos(nombre, direccion, barrio, localidad,
                                   telefono, email, hora_apertura, hora_cierre)
        try:
            with ConexionBD().obtener_session() as session:
                dao = SedeDAO(session)
                sede = self._obtener_o_error(dao, id_sede)
                if dao.existe_nombre(datos['nombre'], sede.id_sede):
                    raise ReglaNegocioError('Ya existe otra sede con ese nombre.')
                for atributo, valor in datos.items():
                    setattr(sede, atributo, valor)
        except IntegrityError as error:
            raise ReglaNegocioError('No se pudo modificar: el nombre ya está registrado.') from error

    def dar_baja_sede(self, id_sede):
        with ConexionBD().obtener_session() as session:
            dao = SedeDAO(session)
            sede = self._obtener_o_error(dao, id_sede)
            if not sede.esta_activa():
                raise ReglaNegocioError('Esta sede ya está dada de baja.')
            motivo = dao.motivo_baja_bloqueada(sede.id_sede)
            if motivo:
                raise ReglaNegocioError(f'No se puede dar de baja la sede. {motivo}')
            sede.dar_baja()  # Baja lógica: conserva préstamos, remitos y ejemplares.

    def reactivar_sede(self, id_sede):
        with ConexionBD().obtener_session() as session:
            sede = self._obtener_o_error(SedeDAO(session), id_sede)
            if sede.esta_activa():
                raise ReglaNegocioError('La sede ya está activa.')
            sede.reactivar()

    @staticmethod
    def _id_valido(id_sede):
        try:
            numero = int(id_sede)
        except (TypeError, ValueError) as error:
            raise ReglaNegocioError('El código de sede debe ser un número entero.') from error
        if numero <= 0:
            raise ReglaNegocioError('El código de sede debe ser positivo.')
        return numero

    def _obtener_o_error(self, dao, id_sede):
        numero = self._id_valido(id_sede)
        sede = dao.obtener(numero)
        if sede is None:
            raise ReglaNegocioError(f'No se encontró la sede con código {numero}.')
        return sede

    @staticmethod
    def _validar_datos(nombre, direccion, barrio, localidad, telefono, email,
                       hora_apertura, hora_cierre):
        valores = {
            'nombre': (nombre or '').strip(),
            'direccion_calle_altura': (direccion or '').strip(),
            'barrio': (barrio or '').strip(),
            'localidad': (localidad or '').strip(),
            'telefono': (telefono or '').strip(),
            'email': (email or '').strip(),
        }
        longitudes = {'nombre': 60, 'direccion_calle_altura': 100, 'barrio': 60,
                     'localidad': 60, 'telefono': 30, 'email': 100}
        etiquetas = {'nombre': 'Nombre', 'direccion_calle_altura': 'Dirección',
                     'barrio': 'Barrio', 'localidad': 'Localidad',
                     'telefono': 'Teléfono', 'email': 'Email'}
        for campo in ('nombre', 'direccion_calle_altura', 'barrio', 'localidad'):
            if not valores[campo]:
                raise ReglaNegocioError(f'El campo {etiquetas[campo]} es obligatorio.')
        for campo, limite in longitudes.items():
            if len(valores[campo]) > limite:
                raise ReglaNegocioError(f'{etiquetas[campo]} admite hasta {limite} caracteres.')
        if valores['email'] and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', valores['email']):
            raise ReglaNegocioError('Ingresá un email válido o dejá el campo vacío.')

        def convertir_hora(valor, campo):
            valor = (valor or '').strip()
            if not re.fullmatch(r'\d{2}:\d{2}', valor):
                raise ReglaNegocioError(f'{campo} debe tener formato HH:MM (ejemplo: 08:00).')
            try:
                return datetime.strptime(valor, '%H:%M').time()
            except ValueError as error:
                raise ReglaNegocioError(f'{campo} no es una hora válida.') from error

        apertura = convertir_hora(hora_apertura, 'Hora de apertura')
        cierre = convertir_hora(hora_cierre, 'Hora de cierre')
        if apertura >= cierre:
            raise ReglaNegocioError('La hora de cierre debe ser posterior a la de apertura.')
        valores['hora_apertura'] = apertura
        valores['hora_cierre'] = cierre
        return valores

    @staticmethod
    def _a_fila(sede):
        return (sede.id_sede, sede.nombre, sede.direccion_calle_altura,
                sede.barrio, sede.localidad, sede.telefono or '', sede.email or '',
                sede.hora_apertura.strftime('%H:%M'),
                sede.hora_cierre.strftime('%H:%M'), sede.estado.value)

    @staticmethod
    def _a_datos(sede):
        return {
            'id_sede': sede.id_sede,
            'nombre': sede.nombre,
            'direccion': sede.direccion_calle_altura,
            'barrio': sede.barrio,
            'localidad': sede.localidad,
            'telefono': sede.telefono or '',
            'email': sede.email or '',
            'hora_apertura': sede.hora_apertura.strftime('%H:%M'),
            'hora_cierre': sede.hora_cierre.strftime('%H:%M'),
            'estado': sede.estado.value,
        }
