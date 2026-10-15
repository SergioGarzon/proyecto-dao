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
                    codigo INTEGER PRIMARY KEY,
                    nombre TEXT,
                    apellido TEXT,
                    fecha_nacimiento TEXT
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
    def conection_database_sqlite3(query_str):
        connection = None
        try:
            connection = sqlite3.connect("base_datos.db")
            cursor = connection.cursor() 
    
            cursor.execute(query_str)
            connection.commit()
    
            print("Información insertada correctamente")
    
        except sqlite3.Error as error:
            if connection:
                connection.rollback()
            print("Error", error)    
        finally:
            if connection:
                connection.close()
