from datetime import date, time

from Entidades import Ejemplar, Libro, Sede, Socio
from Entidades.enums import EstadoSede, EstadoSocio
from Persistencia.conexion import ConexionBD


def cargar_datos_iniciales():
    """Carga datos de ejemplo solo si la base está vacía."""
    with ConexionBD().obtener_session() as session:
        if session.query(Sede).count() > 0:
            return

        centro = Sede(nombre="Sede Centro", direccion_calle_altura="Av. Colón 1200", barrio="Centro",
                      localidad="Córdoba", telefono="351-4000001", email="centro@biblioteca.test",
                      hora_apertura=time(8, 0), hora_cierre=time(20, 0))
        norte = Sede(nombre="Sede Norte", direccion_calle_altura="Av. Rafael Núñez 4500", barrio="Cerro de las Rosas",
                     localidad="Córdoba", telefono="351-4000002", email="norte@biblioteca.test",
                     hora_apertura=time(9, 0), hora_cierre=time(18, 0))
        sur = Sede(nombre="Sede Sur", direccion_calle_altura="Av. Vélez Sarsfield 3100", barrio="Jardín",
                   localidad="Córdoba", hora_apertura=time(9, 0), hora_cierre=time(17, 0),
                   estado=EstadoSede.INACTIVA)

        socios = [
            Socio(legajo_dni=12345, nombre="Federico", apellido="Wedemeyer", fecha_inscripcion=date(2026, 7, 9),
                  domicilio_calle="La Reserva", barrio="Cordoba", localidad="Córdoba"),
            Socio(legajo_dni=38999888, nombre="Martín", apellido="Ruiz", fecha_inscripcion=date(2025, 11, 2),
                  domicilio_calle="Vélez Sarsfield 500", barrio="Nueva Córdoba", localidad="Córdoba",
                  estado=EstadoSocio.INHABILITADO),
            Socio(legajo_dni=40111222, nombre="Lucía", apellido="Gómez", fecha_inscripcion=date(2026, 3, 10),
                  domicilio_calle="Colón 1200", barrio="Centro", localidad="Córdoba"),
        ]

        cien_anios = Libro(isbn="9780307474728", titulo="Cien años de soledad", autor="Gabriel García Márquez",
                           editorial="Sudamericana", anio_publicacion=1967)
        ficciones = Libro(isbn="9788420633121", titulo="Ficciones", autor="Jorge Luis Borges",
                          editorial="Sur", anio_publicacion=1944)
        rayuela = Libro(isbn="9788437604572", titulo="Rayuela", autor="Julio Cortázar",
                        editorial="Sudamericana", anio_publicacion=1963)

        ejemplares = [
            Ejemplar(codigo_inventario="INV-0001", libro=cien_anios, sede=centro),
            Ejemplar(codigo_inventario="INV-0002", libro=cien_anios, sede=centro),
            Ejemplar(codigo_inventario="INV-0003", libro=ficciones, sede=centro),
            Ejemplar(codigo_inventario="INV-0004", libro=ficciones, sede=norte),
            Ejemplar(codigo_inventario="INV-0005", libro=rayuela, sede=norte),
            Ejemplar(codigo_inventario="INV-0006", libro=rayuela, sede=norte),
        ]

        session.add_all([centro, norte, sur] + socios + ejemplares)
