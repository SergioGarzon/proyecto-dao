from datetime import date

from Entidades.enums import EstadoFisico, TipoPrestamo, TipoRemito
from Entidades.excepciones import ReglaNegocioError
from Entidades.multa import Multa
from Entidades.prestamo import Prestamo
from Entidades.remito import Remito
from Persistencia.conexion import ConexionBD
from Persistencia.ejemplar_dao import EjemplarDAO
from Persistencia.prestamo_dao import PrestamoDAO
from Persistencia.remito_dao import RemitoDAO
from Persistencia.sede_dao import SedeDAO
from Persistencia.socio_dao import SocioDAO


class ControladorPrestamo:

    # Campos por los que se puede buscar en la pantalla de préstamos: texto del combo -> campo del DAO
    CAMPOS_BUSQUEDA = {
        "N° préstamo": "numero",
        "Socio (nombre o legajo)": "socio",
        "Libro": "libro",
        "Sede": "sede",
        "Estado": "estado",
    }

    # Consultas para cargar las pantallas
    def consultar_prestamos(self):
        with ConexionBD().obtener_session() as session:
            return [self._a_fila(prestamo) for prestamo in PrestamoDAO(session).listar_recientes()]

    def buscar_prestamos(self, campo, texto):
        if campo not in self.CAMPOS_BUSQUEDA:
            raise ReglaNegocioError("Debe elegir un campo de búsqueda válido.")
        texto = (texto or "").strip()
        if not texto:
            return self.consultar_prestamos()

        campo = self.CAMPOS_BUSQUEDA[campo]
        if campo == "numero" and not texto.isdecimal():
            raise ReglaNegocioError("El número de préstamo debe ser un número.")

        with ConexionBD().obtener_session() as session:
            return [self._a_fila(prestamo) for prestamo in PrestamoDAO(session).buscar(campo, texto)]

    def procesar_vencimientos(self, hoy=None):
        """Inhabilita a los socios con préstamos vencidos. Devuelve cuántos socios cambiaron de estado."""
        hoy = hoy or date.today()
        with ConexionBD().obtener_session() as session:
            socios = {prestamo.socio for prestamo in PrestamoDAO(session).listar_vencidos(hoy)}
            return sum(socio.actualizar_habilitacion(hoy) for socio in socios)

    def consultar_encabezado(self, id_prestamo):
        with ConexionBD().obtener_session() as session:
            prestamo = self.obtener_prestamo(session, id_prestamo)
            return f"N° {prestamo.id_prestamo} - {prestamo.socio.apellido}, {prestamo.socio.nombre}"

    def listar_socios_activos(self):
        with ConexionBD().obtener_session() as session:
            return [(socio.legajo_dni, socio.nombre, socio.apellido)
                    for socio in SocioDAO(session).listar_habilitados()]

    def listar_sedes_activas(self):
        with ConexionBD().obtener_session() as session:
            return [(sede.id_sede, sede.nombre) for sede in SedeDAO(session).listar_activas()]

    def listar_ejemplares_disponibles(self, id_sede):
        with ConexionBD().obtener_session() as session:
            return [(ejemplar.id_ejemplar, ejemplar.codigo_inventario, ejemplar.libro.titulo)
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
            return self.crear_prestamo_en_sesion(session, legajo_dni, id_sede_origen, id_sede_destino,
                                                 tipo, ejemplares, hoy)

    def crear_prestamo_en_sesion(self, session, legajo_dni, id_sede_origen, id_sede_destino, tipo, ejemplares, hoy):
        # Recibe la sesión de quien lo llama, así otro caso de uso (cumplir una reserva) comparte la transacción
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

    def obtener_prestamo(self, session, id_prestamo):
            prestamo = PrestamoDAO(session).obtener(id_prestamo)
            if prestamo is None:
                raise ReglaNegocioError(f"No se encontró un préstamo con id {id_prestamo}.")
            return prestamo

    def consultar_pendientes(self, id_prestamo):
        with ConexionBD().obtener_session() as session:
            prestamo = self.obtener_prestamo(session, id_prestamo)
            prestamo.validar_activo()
            pendientes = []

            for detalle in prestamo.detalles:
                if not detalle.fue_devuelto():
                    pendientes.append((detalle.id_detalle, detalle.id_ejemplar, detalle.ejemplar.codigo_inventario,
                                       detalle.ejemplar.libro.titulo, detalle.estado_fisico_salida.value))
            return pendientes

    def consultar_devueltos(self, id_prestamo):
        with ConexionBD().obtener_session() as session:
            prestamo = self.obtener_prestamo(session, id_prestamo)
            return [(detalle.ejemplar.codigo_inventario, detalle.ejemplar.libro.titulo, detalle.fecha_devolucion,
                     detalle.estado_fisico_devolucion.value)
                    for detalle in prestamo.detalles if detalle.fue_devuelto()]

    def registrar_devolucion(self, id_prestamo, id_detalles, estado_fisico, hoy=None):
        hoy = hoy or date.today()

        if not id_detalles:
            raise ReglaNegocioError("Debe seleccionar uno o más ejemplares para registrar la devolución.")
        fisico = EstadoFisico(estado_fisico)

        with ConexionBD().obtener_session() as session:
            prestamo = self.obtener_prestamo(session, id_prestamo)
            prestamo.validar_activo()

            multas = []
            ejemplares = []
            for id_detalle in id_detalles:
                detalle = prestamo.buscar_detalle(id_detalle)
                detalle.registrar_devolucion(hoy, fisico)
                ejemplares.append(detalle.ejemplar)
                multas.extend(Multa.generar(detalle, hoy))

            session.add_all(multas)

            vuelve_a_origen = fisico not in (EstadoFisico.DESTRUIDO, EstadoFisico.EXTRAVIADO)
            if prestamo.es_interbibliotecario() and vuelve_a_origen:
                remito_dao = RemitoDAO(session)
                remito_dao.guardar(Remito(remito_dao.siguiente_numero(hoy), prestamo, prestamo.sede_destino,
                                          prestamo.sede_origen, TipoRemito.RETORNO, ejemplares, hoy))

            prestamo.verificar_cierre()
            # Las multas nuevas (o devolver un préstamo vencido) cambian la habilitación del socio
            prestamo.socio.actualizar_habilitacion(hoy)
            return sum(multa.monto for multa in multas)  # Devuelve el total de multas generadas

    def _a_fila(self, prestamo):
        socio = prestamo.socio
        libros = ", ".join(detalle.ejemplar.libro.titulo for detalle in prestamo.detalles)
        return (prestamo.id_prestamo, f"{socio.legajo_dni} - {socio.apellido}, {socio.nombre}",
                prestamo.sede_origen.nombre, prestamo.sede_destino.nombre, prestamo.tipo.value,
                prestamo.fecha_prestamo, prestamo.fecha_vencimiento, prestamo.estado.value, libros)
