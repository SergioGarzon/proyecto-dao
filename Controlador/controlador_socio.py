from Persistencia.bd_sqlite import ConectionDAO

class ControladorSocio:
    
    def __init__(self):
        ConectionDAO.crear_tablas()
    
    def consultar_socios(self, query_sql):
        resultados_lista = ConectionDAO.obtener_socios(query_sql)
        return resultados_lista

    def insertar_socios(self, query_sql):
        ConectionDAO.insertar_socios(query_sql)