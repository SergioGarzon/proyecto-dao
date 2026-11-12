
from Entidades.ejemplar import Ejemplar
from Entidades.enums import EstadoEjemplar, EstadoFisico
from Entidades.excepciones import ReglaNegocioError

from Persistencia.conexion import ConexionBD
from Persistencia.ejemplar_dao import EjemplarDAO
from Persistencia.libro_dao import LibroDAO
from Persistencia.sede_dao import SedeDAO


class ControladorEjemplar:

    # Listar los libros para seleccionar uno
    def listar_libros(self):
        with ConexionBD().obtener_session() as session:
            libros = LibroDAO(session).listar_ordenados()

            return [
                (libro.codigo_libro, libro.titulo)
                for libro in libros
            ]

    # Listar las sedes donde podemos registrar ejemplares
    def listar_sedes_activas(self):
        with ConexionBD().obtener_session() as session:
            sedes = SedeDAO(session).listar_activas()

            return [
                (sede.id_sede, sede.nombre)
                for sede in sedes
            ]

    # Consultar ejemplares de un libro
    def consultar_ejemplares(self, codigo_libro):
        with ConexionBD().obtener_session() as session:
            ejemplares = EjemplarDAO(session).listar_por_libro(
                codigo_libro
            )

            return [
                (
                    ejemplar.id_ejemplar,
                    ejemplar.codigo_inventario,
                    ejemplar.libro.titulo,
                    ejemplar.sede.nombre,
                    ejemplar.estado.value,
                    ejemplar.estado_fisico.value
                )
                for ejemplar in ejemplares
            ]

    # Registrar un nuevo ejemplar
    def registrar_ejemplar(self, codigo_libro, id_sede, codigo_inventario):

        codigo_inventario = codigo_inventario.strip().upper()

        if not codigo_inventario:
            raise ReglaNegocioError(
                "El código de inventario es obligatorio."
            )

        if len(codigo_inventario) > 30:
            raise ReglaNegocioError(
                "El código de inventario no puede superar 30 caracteres."
            )

        try:
            codigo_libro = int(codigo_libro)
            id_sede = int(id_sede)
        except (ValueError, TypeError):
            raise ReglaNegocioError(
                "Debe seleccionar un libro y una sede válidos."
            )

        if codigo_libro <= 0 or id_sede <= 0:
            raise ReglaNegocioError(
                "Debe seleccionar un libro y una sede válidos."
            )

        with ConexionBD().obtener_session() as session:

            libro = LibroDAO(session).obtener(codigo_libro)

            if libro is None:
                raise ReglaNegocioError(
                    "El libro seleccionado no existe."
                )

            sede = SedeDAO(session).obtener(id_sede)

            if sede is None:
                raise ReglaNegocioError(
                    "La sede seleccionada no existe."
                )

            # No se pueden registrar ejemplares en sedes dadas de baja
            sede.validar_activa()

            ejemplar_dao = EjemplarDAO(session)

            # Evitar códigos de inventario repetidos
            if ejemplar_dao.buscar_por_codigo(codigo_inventario):
                raise ReglaNegocioError(
                    "Ya existe un ejemplar con ese código de inventario."
                )

            nuevo_ejemplar = Ejemplar(
                codigo_inventario=codigo_inventario,
                codigo_libro=codigo_libro,
                id_sede=id_sede,
                estado=EstadoEjemplar.DISPONIBLE,
                estado_fisico=EstadoFisico.BUENO
            )

            ejemplar_dao.guardar(nuevo_ejemplar)

            session.flush()

            return nuevo_ejemplar.id_ejemplar
