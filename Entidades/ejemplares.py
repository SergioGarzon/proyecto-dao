class Ejemplar:

    _codigo_inventario = None
    _libro = None
    _sede = None
    _estado_fisico = None
    _disponible = None

    def __init__(self, codigo_inventario, libro, sede, estado_fisico, disponible=True):
        self._codigo_inventario = codigo_inventario
        self._libro = libro          
        self._sede = sede            
        self._estado_fisico = estado_fisico
        self._disponible = disponible

    # Setters
    @_codigo_inventario.setter
    def codigo_inventario(self, codigo_inventario):
        self._codigo_inventario = codigo_inventario

    @_libro.setter
    def libro(self, libro):
        self._libro = libro

    @_sede.setter
    def sede(self, sede):
        self._sede = sede

    @_estado_fisico.setter
    def estado_fisico(self, estado_fisico):
        self._estado_fisico = estado_fisico

    @_disponible.setter
    def disponible(self, disponible):
        self._disponible = disponible

    # Getters
    @property
    def codigo_inventario(self):
        return self._codigo_inventario

    @property
    def libro(self):
        return self._libro

    @property
    def sede(self):
        return self._sede

    @property
    def estado_fisico(self):
        return self._estado_fisico

    @property
    def disponible(self):
        return self._disponible