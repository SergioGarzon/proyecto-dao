from datetime import date
from Persistencia.bd_sqlite import ConectionDAO
from Entidades.prestamo import Prestamo
from Entidades.socio import Socio
from Entidades.sede import Sede
from Entidades.ejemplar import Ejemplar


class ControladorPrestamo:

    def __init__(self):
        ConectionDAO.crear_tablas()

    # Consultas para cargar las pantallas
    def consultar_prestamos(self):
        query = '''
            SELECT p.id_prestamo, p.socio_legajo_dni, p.sede_origen, p.sede_destino, p.tipo,
                   p.fecha_prestamo, p.fecha_devolucion, p.estado,
                   GROUP_CONCAT(d.id_ejemplar, ', ')
            FROM prestamos p
            LEFT JOIN detalles_prestamo d ON d.id_prestamo = p.id_prestamo
            GROUP BY p.id_prestamo
            ORDER BY p.id_prestamo DESC
        '''
        return ConectionDAO.obtener_prestamos(query)

    def listar_socios_activos(self):
        return ConectionDAO.obtener_prestamos(
            "SELECT legajo_dni, nombre, apellido FROM socios WHERE estado_socio = 'Activo' ORDER BY apellido")

    def listar_sedes_activas(self):
        return ConectionDAO.obtener_prestamos(
            "SELECT id_sede FROM sedes WHERE estado = 'Activa' ORDER BY id_sede")

    def listar_ejemplares_disponibles(self, id_sede):
        return ConectionDAO.consultar_todos(
            "SELECT id_ejemplar, codigo_libro FROM ejemplares WHERE estado = 'Disponible' AND id_sede = ? ORDER BY id_ejemplar",
            (id_sede,))

    def registrar_prestamo(self, legajo_dni, id_sede_origen, id_sede_destino, tipo, fecha_prestamo, ejemplares):

        # Validamos que los ejemplares sean válidos
        if not ejemplares:
            raise ValueError("No se puede registrar un préstamo sin ejemplares.")

        if len(ejemplares) != len(set(ejemplares)):
            raise ValueError("No se pueden registrar ejemplares duplicados en un préstamo.")

        # Validamos que las sedes sean válidas para el tipo de préstamo
        if tipo == "Local" and id_sede_origen != id_sede_destino:
            raise ValueError("Para préstamos locales, la sede de origen y destino deben ser la misma.")

        if tipo == "Interbibliotecario" and id_sede_origen == id_sede_destino:
            raise ValueError("Para préstamos interbibliotecarios, la sede de origen y destino deben ser diferentes.")

        # Válidamos al socio
        socio = ConectionDAO.consultar_uno("SELECT * FROM socios WHERE legajo_dni = ?", (legajo_dni,))
        if socio is None:
            raise ValueError(f"No se encontró un socio con legajo/dni {legajo_dni}.")

        if socio[7] != "Activo":
            raise ValueError(f"El socio con legajo/dni {legajo_dni} no está activo.")

        # Validamos las sedes (existen y no están dadas de baja)
        sede_origen = self._obtener_sede_activa(id_sede_origen)
        sede_destino = self._obtener_sede_activa(id_sede_destino)

        # Validamos la existencia y disponibilidad de los ejemplares
        lista_ejemplares = []
        for id_ejemplar in ejemplares:
            ejemplar = ConectionDAO.consultar_uno("SELECT estado, id_sede FROM ejemplares WHERE id_ejemplar = ?", (id_ejemplar,))
            if ejemplar is None:
                raise ValueError(f"No se encontró un ejemplar con id {id_ejemplar}.")
            estado_ejemplar, sede_ejemplar = ejemplar
            if estado_ejemplar != "Disponible":
                raise ValueError(f"El ejemplar con id {id_ejemplar} no está disponible para préstamo.")
            if sede_ejemplar != id_sede_origen:
                raise ValueError(f"El ejemplar con id {id_ejemplar} no pertenece a la sede de origen {id_sede_origen}.")
            lista_ejemplares.append(Ejemplar(id_ejemplar, None, sede_origen, estado=estado_ejemplar))

        # Creamos el objeto Prestamo
        prestamo = Prestamo(
            id_prestamo=None,
            socio=Socio(*socio),
            sede_origen=sede_origen,
            sede_destino=sede_destino,
            tipo=tipo,
            fecha_prestamo=date.today(),
            fecha_devolucion=None,
            estado="Activo"
        )

        nuevo_estado = "Prestado" if tipo == "Local" else "En tránsito"
        for ejemplar in lista_ejemplares:
            ejemplar.estado = nuevo_estado
            prestamo.agregar_detalle(ejemplar)

        # 6. Guardar (préstamo + detalles + estados, todo junto)
        ConectionDAO.insertar_prestamo(prestamo)
        return prestamo

    def _obtener_sede_activa(self, id_sede):
        sede = ConectionDAO.consultar_uno("SELECT id_sede, estado FROM sedes WHERE id_sede = ?", (id_sede,))
        if sede is None:
            raise ValueError(f"No se encontró una sede con id {id_sede}.")
        codigo_sede, estado_sede = sede
        if estado_sede != "Activa":
            raise ValueError(f"La sede con id {id_sede} está dada de baja.")
        # La tabla sedes por ahora solo tiene id y estado, el resto de los datos van en None
        return Sede(codigo_sede, None, None, None, None, None, None, None, estado_sede)