import sqlite3

class ConectionDAO:
    
    @staticmethod
    def crear_tablas():
        connection = None
        try:
            connection = sqlite3.connect("base_datos.db")
            cursor = connection.cursor()
            connection.execute("PRAGMA foreign_keys = ON")
            
            query_tabla_socios = '''
                CREATE TABLE IF NOT EXISTS socios (
                    legajo_dni INTEGER PRIMARY KEY,
                    nombre TEXT,
                    apellido TEXT,
                    fecha_inscripcion TEXT,
                    domicilio_calle TEXT,
                    barrio TEXT,
                    localidad TEXT,
                    estado_socio TEXT
                )
            '''
            query_tabla_prestamos = '''
                CREATE TABLE IF NOT EXISTS prestamos (
                    id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
                    socio_legajo_dni INTEGER NOT NULL,
                    sede_origen INTEGER NOT NULL,
                    sede_destino INTEGER NOT NULL,
                    fecha_prestamo TEXT,
                    fecha_devolucion TEXT,
                    tipo TEXT,
                    estado TEXT,
                    FOREIGN KEY (socio_legajo_dni) REFERENCES socios(legajo_dni),
                    FOREIGN KEY (sede_origen)  REFERENCES sedes(id_sede),
                    FOREIGN KEY (sede_destino) REFERENCES sedes(id_sede)
                )
                '''

            query_tabla_ejemplares = '''
                CREATE TABLE IF NOT EXISTS ejemplares (
                    id_ejemplar INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_libro INTEGER NOT NULL,
                    id_sede INTEGER NOT NULL,
                    estado TEXT,
                    FOREIGN KEY (codigo_libro) REFERENCES libros(codigo_libro),
                    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede))
                '''

            query_tabla_sedes = '''
                CREATE TABLE IF NOT EXISTS sedes (
                    id_sede INTEGER PRIMARY KEY AUTOINCREMENT,
                    estado TEXT)
                '''

            query_table_detalles_prestamos = '''
            CREATE TABLE IF NOT EXISTS detalles_prestamo (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_prestamo INTEGER NOT NULL,
            id_ejemplar INTEGER NOT NULL,
            estado_material TEXT,
            FOREIGN KEY (id_prestamo)  REFERENCES prestamos(id_prestamo) ON DELETE CASCADE,
            FOREIGN KEY (id_ejemplar) REFERENCES ejemplares(id_ejemplar))
            '''

            query_tabla_libros = '''
            CREATE TABLE IF NOT EXISTS libros (
                codigo_libro INTEGER PRIMARY KEY AUTOINCREMENT)
            '''

            cursor.execute(query_tabla_socios)
            cursor.execute(query_tabla_sedes)
            cursor.execute(query_tabla_libros)
            cursor.execute(query_tabla_ejemplares)
            cursor.execute(query_tabla_prestamos)
            cursor.execute(query_table_detalles_prestamos)
            connection.commit()
            print("Tablas creadas con éxito.")
            
        except sqlite3.Error as error:
            print("Error al crear las tablas:", error)
        finally:
            if connection:
                connection.close()

    @staticmethod
    def insertar_socios(query_str):
        connection = None
        try:
            connection = sqlite3.connect("base_datos.db")
            cursor = connection.cursor() 
    
            cursor.execute(query_str)
            connection.commit()
            print("Operación de escritura exitosa")
    
        except sqlite3.Error as error:
            if connection:
                connection.rollback()
            print("Error en escritura:", error)    
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_socios(query_str):
        connection = None
        resultados = [] 
        try:
            connection = sqlite3.connect("base_datos.db")
            cursor = connection.cursor()
            
            cursor.execute(query_str)
            resultados = cursor.fetchall() # Esto esta en el documento es para traer los datos de la tabla
            
        except sqlite3.Error as error:
            print("Error al consultar los socios:", error)
        finally:
            if connection:
                connection.close()
                
        return resultados

    @staticmethod
    def insertar_prestamo(prestamo):
        connection = None

        try:
            connection = sqlite3.connect("base_datos.db")
            connection.execute("PRAGMA foreign_keys = ON")
            cursor = connection.cursor()

            query_prestamo = '''
                INSERT INTO prestamos (socio_legajo_dni, sede_origen, sede_destino,
                                    fecha_prestamo, fecha_devolucion, tipo, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(query_prestamo, (
                prestamo.socio.legajo_dni,
                prestamo.sede_origen.codigo_sede,
                prestamo.sede_destino.codigo_sede,
                prestamo.fecha_prestamo,
                prestamo.fecha_devolucion,
                prestamo.tipo,
                prestamo.estado
            ))

            id_nuevo = cursor.lastrowid

            query_detalle = '''
                INSERT INTO detalles_prestamo (id_prestamo, id_ejemplar, estado_material)
                VALUES (?, ?, ?)
            '''
            for detalle in prestamo.detalle_prestamo:
                cursor.execute(query_detalle, (
                    id_nuevo,
                    detalle.ejemplar.id_ejemplar,
                    detalle.estado_material
                ))
                cursor.execute(
                    "UPDATE ejemplares SET estado = ? WHERE id_ejemplar = ?",
                    (detalle.ejemplar.estado, detalle.ejemplar.id_ejemplar))

            connection.commit()
            prestamo.id_prestamo = id_nuevo
            print("Préstamo registrado con éxito")
            return id_nuevo

        except sqlite3.Error as error:
            # Si falló cualquier insert, no queda nada guardado a medias
            if connection:
                connection.rollback()
            print("Error al registrar el préstamo:", error)
            raise
        finally:
            if connection:
                connection.close()

    @staticmethod
    def consultar_uno(query_str, parametros=()):
        connection = None
        try:
            connection = sqlite3.connect("base_datos.db")
            cursor = connection.cursor()
            cursor.execute(query_str, parametros)
            return cursor.fetchone()  # Devuelve una tupla, o None si no existe
        except sqlite3.Error as error:
            print("Error en la consulta:", error)
            return None
        finally:
            if connection:
                connection.close()

    @staticmethod
    def obtener_prestamos(query_str):
        connection = None
        resultados = [] 
        try:
            connection = sqlite3.connect("base_datos.db")
            cursor = connection.cursor()
            
            cursor.execute(query_str)
            resultados = cursor.fetchall()
            
        except sqlite3.Error as error:
            print("Error al consultar los prestamos:", error)
        finally:
            if connection:
                connection.close()
                
        return resultados