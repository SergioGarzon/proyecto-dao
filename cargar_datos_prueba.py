"""Llena una base vacía con datos inventados para probar el sistema.

Simula seis meses de movimientos, día por día, usando las mismas reglas de las entidades.
Así los estados quedan coherentes y hay datos para probar pantallas y reportes.

Uso: python cargar_datos_prueba.py
"""
import random
from collections import defaultdict
from datetime import date, datetime, time, timedelta

from Entidades import Ejemplar, Libro, Multa, Prestamo, Remito, Reserva, Sede, Socio
from Entidades.enums import EstadoFisico, EstadoReserva, EstadoSede, EstadoSocio, TipoPrestamo, TipoRemito
from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import ConexionBD
from Persistencia.remito_dao import RemitoDAO

DIAS_SIMULADOS = 180
CANTIDAD_SOCIOS = 80
CANTIDAD_RESERVAS = 50
PROBABILIDAD_INTERBIBLIOTECARIO = 0.4
PROBABILIDAD_INCIDENCIA = 0.1
PROBABILIDAD_NO_DEVUELVE = 0.04
PROBABILIDAD_DEVOLUCION_PARCIAL = 0.15
PROBABILIDAD_PAGA_MULTA = 0.9

SEDES = [
    ("Sede Centro", "Av. Colón 1200", "Centro", "Córdoba", EstadoSede.ACTIVA),
    ("Sede Norte", "Av. Rafael Núñez 4500", "Cerro de las Rosas", "Córdoba", EstadoSede.ACTIVA),
    ("Sede Este", "Av. Sabattini 2500", "Empalme", "Córdoba", EstadoSede.ACTIVA),
    ("Sede Oeste", "Av. Fuerza Aérea 3100", "Alto Alberdi", "Córdoba", EstadoSede.ACTIVA),
    ("Sede Carlos Paz", "Av. San Martín 800", "Centro", "Villa Carlos Paz", EstadoSede.ACTIVA),
    ("Sede Sur", "Av. Vélez Sarsfield 3100", "Jardín", "Córdoba", EstadoSede.INACTIVA),
]

LIBROS = [
    ("Cien años de soledad", "Gabriel García Márquez", "Sudamericana", 1967),
    ("El amor en los tiempos del cólera", "Gabriel García Márquez", "Oveja Negra", 1985),
    ("Ficciones", "Jorge Luis Borges", "Sur", 1944),
    ("El Aleph", "Jorge Luis Borges", "Losada", 1949),
    ("Rayuela", "Julio Cortázar", "Sudamericana", 1963),
    ("Bestiario", "Julio Cortázar", "Sudamericana", 1951),
    ("Sobre héroes y tumbas", "Ernesto Sabato", "Fabril", 1961),
    ("El túnel", "Ernesto Sabato", "Sur", 1948),
    ("Martín Fierro", "José Hernández", "Pampa", 1872),
    ("Facundo", "Domingo F. Sarmiento", "El Progreso", 1845),
    ("La invención de Morel", "Adolfo Bioy Casares", "Losada", 1940),
    ("Pedro Páramo", "Juan Rulfo", "Fondo de Cultura", 1955),
    ("La ciudad y los perros", "Mario Vargas Llosa", "Seix Barral", 1963),
    ("La casa de los espíritus", "Isabel Allende", "Plaza & Janés", 1982),
    ("Don Quijote de la Mancha", "Miguel de Cervantes", "Francisco de Robles", 1605),
    ("Crimen y castigo", "Fiódor Dostoyevski", "El Mensajero Ruso", 1866),
    ("Orgullo y prejuicio", "Jane Austen", "T. Egerton", 1813),
    ("1984", "George Orwell", "Secker & Warburg", 1949),
    ("Rebelión en la granja", "George Orwell", "Secker & Warburg", 1945),
    ("Fahrenheit 451", "Ray Bradbury", "Ballantine", 1953),
    ("Crónicas marcianas", "Ray Bradbury", "Doubleday", 1950),
    ("Un mundo feliz", "Aldous Huxley", "Chatto & Windus", 1932),
    ("El principito", "Antoine de Saint-Exupéry", "Reynal & Hitchcock", 1943),
    ("El extranjero", "Albert Camus", "Gallimard", 1942),
    ("La metamorfosis", "Franz Kafka", "Kurt Wolff", 1915),
    ("Frankenstein", "Mary Shelley", "Lackington", 1818),
    ("Drácula", "Bram Stoker", "Constable", 1897),
    ("Moby Dick", "Herman Melville", "Harper & Brothers", 1851),
    ("El gran Gatsby", "F. Scott Fitzgerald", "Scribner", 1925),
    ("Yo, robot", "Isaac Asimov", "Gnome Press", 1950),
    ("Fundación", "Isaac Asimov", "Gnome Press", 1951),
    ("Dune", "Frank Herbert", "Chilton", 1965),
    ("El señor de los anillos", "J. R. R. Tolkien", "Allen & Unwin", 1954),
    ("El hobbit", "J. R. R. Tolkien", "Allen & Unwin", 1937),
    ("El nombre de la rosa", "Umberto Eco", "Bompiani", 1980),
    ("Patas de la bestia", "Mariana Enríquez", "Anagrama", 2016),
    ("Las cosas que perdimos en el fuego", "Mariana Enríquez", "Anagrama", 2016),
    ("El eternauta", "Héctor G. Oesterheld", "Frontera", 1957),
    ("Mafalda: todas las tiras", "Quino", "De la Flor", 1993),
    ("Clean Code", "Robert C. Martin", "Prentice Hall", 2008),
]

NOMBRES = ["Ana", "Bruno", "Camila", "Diego", "Elena", "Facundo", "Gabriela", "Hernán", "Inés", "Joaquín",
           "Julieta", "Lautaro", "Lucía", "Martín", "Natalia", "Nicolás", "Paula", "Ramiro", "Sofía", "Tomás"]
APELLIDOS = ["Acosta", "Benítez", "Castro", "Díaz", "Fernández", "Gómez", "Herrera", "Juárez", "López", "Martínez",
             "Núñez", "Ortiz", "Pereyra", "Quiroga", "Ríos", "Sosa", "Torres", "Vega", "Zárate", "O'Brien"]
BARRIOS = ["Centro", "Nueva Córdoba", "General Paz", "Alberdi", "Cofico", "Güemes", "Jardín", "Argüello"]


def crear_catalogo(session, azar):
    sedes = [Sede(nombre=nombre, direccion_calle_altura=direccion, barrio=barrio, localidad=localidad,
                  telefono=f"351-40000{numero:02d}", email=f"sede{numero}@biblioteca.test",
                  hora_apertura=time(8, 0), hora_cierre=time(20, 0), estado=estado)
             for numero, (nombre, direccion, barrio, localidad, estado) in enumerate(SEDES, start=1)]

    libros = [Libro(isbn=f"978950{numero:07d}", titulo=titulo, autor=autor, editorial=editorial, anio_publicacion=anio)
              for numero, (titulo, autor, editorial, anio) in enumerate(LIBROS, start=1)]

    ejemplares = []
    for libro in libros:
        for sede in sedes:
            for _ in range(azar.randint(0, 3)):
                fisico = azar.choice((EstadoFisico.BUENO, EstadoFisico.BUENO, EstadoFisico.REGULAR))
                ejemplares.append(Ejemplar(codigo_inventario=f"INV-{len(ejemplares) + 1:05d}", libro=libro,
                                           sede=sede, estado_fisico=fisico))

    session.add_all(sedes + libros + ejemplares)
    session.flush()
    return sedes, libros, ejemplares


def crear_socios(session, azar, hoy):
    socios = []
    for legajo in azar.sample(range(20000000, 45000000), CANTIDAD_SOCIOS):
        socios.append(Socio(legajo_dni=legajo, nombre=azar.choice(NOMBRES), apellido=azar.choice(APELLIDOS),
                            fecha_inscripcion=hoy - timedelta(days=DIAS_SIMULADOS + azar.randint(1, 700)),
                            domicilio_calle=f"Calle {azar.randint(1, 200)} {azar.randint(100, 4000)}",
                            barrio=azar.choice(BARRIOS), localidad="Córdoba"))

    # Unos pocos no pueden pedir préstamos, para probar esas validaciones
    socios[0].estado = EstadoSocio.INHABILITADO
    socios[1].estado = EstadoSocio.INHABILITADO
    socios[2].estado = EstadoSocio.INHABILITADO
    socios[3].estado = EstadoSocio.BAJA
    socios[4].estado = EstadoSocio.BAJA

    session.add_all(socios)
    session.flush()
    return socios


class Simulacion:
    """Recorre los días en orden. Lo que cae después de hoy no se ejecuta y queda en curso."""

    def __init__(self, session, azar, hoy, sedes, ejemplares, socios):
        self.session = session
        self.azar = azar
        self.hoy = hoy
        self.sedes = [sede for sede in sedes if sede.esta_activa()]
        self.ejemplares = ejemplares
        self.socios = [socio for socio in socios if socio.esta_habilitado()]
        self.agenda = defaultdict(list)

    def programar(self, fecha, accion, *datos):
        self.agenda[fecha].append((accion, datos))

    def ejecutar(self):
        for dias_atras in range(DIAS_SIMULADOS, -1, -1):
            fecha = self.hoy - timedelta(days=dias_atras)
            for accion, datos in self.agenda.pop(fecha, []):
                accion(*datos)
            for _ in range(self.azar.randint(0, 3)):
                self.nuevo_prestamo(fecha)
            if dias_atras < 4:  # Asegura remitos en camino y préstamos pendientes de envío
                self.nuevo_prestamo(fecha, es_inter=True)
                self.nuevo_prestamo(fecha, es_inter=True)

    def nuevo_prestamo(self, fecha, es_inter=False):
        socio = self.azar.choice(self.socios)
        origen = self.azar.choice(self.sedes)
        disponibles = [ejemplar for ejemplar in self.ejemplares
                       if ejemplar.pertenece_a(origen) and ejemplar.esta_disponible()]
        try:
            socio.validar_habilitado(fecha)
        except ReglaNegocioError:
            return
        if not disponibles:
            return

        es_inter = es_inter or self.azar.random() < PROBABILIDAD_INTERBIBLIOTECARIO
        destino = self.azar.choice([sede for sede in self.sedes if sede != origen]) if es_inter else origen
        tipo = TipoPrestamo.INTERBIBLIOTECARIO if es_inter else TipoPrestamo.LOCAL
        prestamo = Prestamo(socio=socio, sede_origen=origen, sede_destino=destino, tipo=tipo, fecha_prestamo=fecha)
        prestamo.validar_sedes()
        self.session.add(prestamo)

        elegidos = self.azar.sample(disponibles, min(len(disponibles), self.azar.choice((1, 1, 1, 2, 3))))
        for ejemplar in elegidos:
            prestamo.agregar_ejemplar(ejemplar)

        if es_inter:
            for ejemplar in elegidos:
                ejemplar.preparar_envio()
            remito = self.crear_remito(prestamo, origen, destino, TipoRemito.IDA, elegidos, fecha)
            self.programar(fecha + timedelta(days=1), self.despachar, remito, fecha + timedelta(days=1))
        else:
            prestamo.activar(fecha)
            self.programar_devoluciones(prestamo, fecha)

    def crear_remito(self, prestamo, origen, destino, tipo, ejemplares, fecha):
        remito = Remito(RemitoDAO(self.session).siguiente_numero(fecha), prestamo, origen, destino,
                        tipo, ejemplares, fecha)
        self.session.add(remito)
        self.fechar_ultimo_cambio(remito, fecha)
        return remito

    def fechar_ultimo_cambio(self, remito, fecha):
        # El historial se guarda con la hora actual: acá lo llevamos al día simulado
        remito.historial[-1].fecha_hora = datetime.combine(fecha, time(self.azar.randint(8, 19), 0))

    def despachar(self, remito, fecha):
        remito.despachar()
        self.fechar_ultimo_cambio(remito, fecha)
        self.programar(fecha + timedelta(days=1), self.iniciar_transito, remito, fecha + timedelta(days=1))

    def iniciar_transito(self, remito, fecha):
        remito.iniciar_transito()
        self.fechar_ultimo_cambio(remito, fecha)
        llegada = fecha + timedelta(days=self.azar.randint(1, 4))
        if remito.tipo == TipoRemito.IDA and self.azar.random() < PROBABILIDAD_INCIDENCIA:
            self.programar(llegada, self.registrar_incidencia, remito, llegada)
        else:
            self.programar(llegada, self.recibir, remito, llegada)

    def registrar_incidencia(self, remito, fecha):
        if self.azar.random() < 0.5:
            remito.reportar_danio()
        else:
            remito.reportar_extravio()
        self.fechar_ultimo_cambio(remito, fecha)

    def recibir(self, remito, fecha):
        remito.recibir()
        self.fechar_ultimo_cambio(remito, fecha)
        if remito.tipo == TipoRemito.IDA:
            remito.prestamo.activar(fecha)  # Al recibir se activó con la fecha real: usamos la simulada
            self.programar_devoluciones(remito.prestamo, fecha)

    def programar_devoluciones(self, prestamo, fecha):
        if self.azar.random() < PROBABILIDAD_NO_DEVUELVE:
            return  # Queda activo y, con el tiempo, vencido
        dias = self.azar.randint(5, 17)
        detalles = prestamo.detalles
        if len(detalles) > 1 and self.azar.random() < PROBABILIDAD_DEVOLUCION_PARCIAL:
            detalles = detalles[:1]  # El resto no vuelve y el préstamo sigue activo
        for detalle in detalles:
            # A veces un ejemplar vuelve después que los demás
            extra = self.azar.randint(1, 6) if self.azar.random() < 0.3 else 0
            devolucion = fecha + timedelta(days=dias + extra)
            self.programar(devolucion, self.devolver, detalle, devolucion)

    def devolver(self, detalle, fecha):
        fisico = self.azar.choices(
            (EstadoFisico.BUENO, EstadoFisico.REGULAR, EstadoFisico.DANADO, EstadoFisico.DESTRUIDO,
             EstadoFisico.EXTRAVIADO), weights=(70, 20, 6, 2, 2))[0]
        prestamo = detalle.prestamo
        detalle.registrar_devolucion(fecha, fisico)
        prestamo.verificar_cierre()

        for multa in Multa.generar(detalle, fecha):
            self.session.add(multa)
            if self.azar.random() < PROBABILIDAD_PAGA_MULTA:
                pago = fecha + timedelta(days=self.azar.randint(1, 15))
                self.programar(pago, multa.pagar, pago)

        vuelve_a_origen = fisico not in (EstadoFisico.DESTRUIDO, EstadoFisico.EXTRAVIADO)
        if prestamo.es_interbibliotecario() and vuelve_a_origen:
            remito = self.crear_remito(prestamo, prestamo.sede_destino, prestamo.sede_origen, TipoRemito.RETORNO,
                                       [detalle.ejemplar], fecha)
            self.programar(fecha + timedelta(days=1), self.despachar, remito, fecha + timedelta(days=1))


def crear_reservas(session, azar, hoy, sedes, libros, socios):
    sedes_activas = [sede for sede in sedes if sede.esta_activa()]
    socios_activos = [socio for socio in socios if socio.esta_habilitado()]

    for _ in range(CANTIDAD_RESERVAS):
        libro = azar.choice(libros)
        sede = azar.choice(sedes_activas)
        desenlace = azar.choice(("pendiente", "asignada", "cumplida", "cancelada", "vencida"))
        vigente = desenlace in ("pendiente", "asignada")
        fecha = hoy - timedelta(days=azar.randint(0, 2) if vigente else azar.randint(5, 90))
        reserva = Reserva(socio=azar.choice(socios_activos), libro=libro, sede_retiro=sede, fecha_reserva=fecha,
                          estado=EstadoReserva.PENDIENTE)
        session.add(reserva)

        if desenlace == "cancelada":
            reserva.cancelar()
            continue
        disponibles = libro.ejemplares_disponibles(sede.id_sede)
        if desenlace == "pendiente" or not disponibles:
            continue

        reserva.asignar_ejemplar(disponibles[0], fecha)
        if desenlace == "cumplida":
            reserva.cumplir(fecha)
        elif desenlace == "vencida":
            reserva.vencer(hoy)


def cargar_datos_prueba(hoy=None, semilla=2026):
    hoy = hoy or date.today()
    azar = random.Random(semilla)  # Con la misma semilla salen siempre los mismos datos

    ConexionBD().crear_tablas()
    with ConexionBD().obtener_session() as session:
        if session.query(Sede).count() > 0:
            print("La base ya tiene datos. Cerrá el sistema, borrá biblioteca.db y volvé a ejecutar el script.")
            return False

        sedes, libros, ejemplares = crear_catalogo(session, azar)
        socios = crear_socios(session, azar, hoy)
        Simulacion(session, azar, hoy, sedes, ejemplares, socios).ejecutar()
        crear_reservas(session, azar, hoy, sedes, libros, socios)

        session.flush()
        for entidad in (Sede, Socio, Libro, Ejemplar, Prestamo, Remito, Multa, Reserva):
            print(f"{entidad.__name__}: {session.query(entidad).count()}")
    return True


if __name__ == "__main__":
    cargar_datos_prueba()
