from datetime import date

from Entidades.enums import TipoPrestamo, TipoRemito
from Entidades.excepciones import ReglaNegocioError
from Entidades.prestamo import Prestamo
from Entidades.remito import Remito
from Persistencia.conexion import ConexionBD
from Persistencia.ejemplar_dao import EjemplarDAO
from Persistencia.prestamo_dao import PrestamoDAO
from Persistencia.remito_dao import RemitoDAO
from Persistencia.sede_dao import SedeDAO
from Persistencia.socio_dao import SocioDAO


class ControladorPrestamo:

    # Consultas para cargar las pantallas
    def consultar_prestamos(self):
        with ConexionBD().obtener_session() as session:
            filas = []
            for prestamo in PrestamoDAO(session).listar_recientes():
                ejemplares = ", ".join(str(detalle.id_ejemplar) for detalle in prestamo.detalles)
                filas.append((prestamo.id_prestamo, prestamo.legajo_dni, prestamo.id_sede_origen,
                              prestamo.id_sede_destino, prestamo.tipo.value, prestamo.fecha_prestamo,
                              prestamo.fecha_vencimiento, prestamo.estado.value, ejemplares))
            return filas

    def listar_socios_activos(self):
        with ConexionBD().obtener_session() as session:
            return [(socio.legajo_dni, socio.nombre, socio.apellido)
                    for socio in SocioDAO(session).listar_habilitados()]

    def listar_sedes_activas(self):
        with ConexionBD().obtener_session() as session:
            return [(sede.id_sede,) for sede in SedeDAO(session).listar_activas()]

    def listar_ejemplares_disponibles(self, id_sede):
        with ConexionBD().obtener_session() as session:
            return [(ejemplar.id_ejemplar, ejemplar.codigo_libro)
                    for ejemplar in EjemplarDAO(session).disponibles_por_sede(id_sede)]

    def registrar_prestamo(self, legajo_dni, id_sede_origen, id_sede_destino, tipo, ejemplares, hoy=None):
        hoy = hoy or date.today()

        # Validamos que los ejemplares sean válidos
        if not ejemplares:
            raise ReglaNegocioError("No se puede registrar un préstamo sin ejemplares.")

        if len(ejemplares) != len(set(ejemplares)):
            raise ReglaNegocioError("No se pueden registrar ejemplares duplicados en un préstamo.")

        # Toda la operación usa una sesión: si algo falla, no queda nada guardado a medias
        with ConexionBD().obtener_session() as session:
            socio = SocioDAO(session).obtener(legajo_dni)
            if socio is None:
                raise ReglaNegocioError(f"No se encontró un socio con legajo/dni {legajo_dni}.")
            socio.validar_habilitado(hoy)

            sede_dao = SedeDAO(session)
            sede_origen = sede_dao.obtener(id_sede_origen)
            sede_destino = sede_dao.obtener(id_sede_destino)
            if sede_origen is None or sede_destino is None:
                raise ReglaNegocioError("No se encontró la sede de origen o de destino.")

            prestamo = Prestamo(socio=socio, sede_origen=sede_origen, sede_destino=sede_destino,
                                tipo=TipoPrestamo(tipo), fecha_prestamo=hoy)
            prestamo.validar_sedes()
            PrestamoDAO(session).guardar(prestamo)

            ejemplar_dao = EjemplarDAO(session)
            lista_ejemplares = []
            for id_ejemplar in ejemplares:
                ejemplar = ejemplar_dao.obtener(id_ejemplar)
                if ejemplar is None:
                    raise ReglaNegocioError(f"No se encontró un ejemplar con id {id_ejemplar}.")
                prestamo.agregar_ejemplar(ejemplar)
                lista_ejemplares.append(ejemplar)

            if prestamo.es_interbibliotecario():
                for ejemplar in lista_ejemplares:
                    ejemplar.preparar_envio()
                remito_dao = RemitoDAO(session)
                remito_dao.guardar(Remito(remito_dao.siguiente_numero(hoy), prestamo, sede_origen, sede_destino,
                                          TipoRemito.IDA, lista_ejemplares, hoy))
            else:
                prestamo.activar(hoy)

            session.flush()  # Asigna el id para mostrarlo en pantalla
            return prestamo.id_prestamo
