import sqlite3

class ConectionDAO:
    
    @staticmethod
    def crear_tablas():
        connection = None
        try:
            connection = sqlite3.connect("base_datos.db")
            cursor = connection.cursor()
            
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
            cursor.execute(query_tabla_socios)
            connection.commit()
            print("Tabla creada con éxito.")
            
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
