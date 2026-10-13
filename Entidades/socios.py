class Socios:
    _id = None
    _nombre = None
    _apellido = None
    _estado = None

    def __init__(self):
        self._id = None
        self._nombre = None
        self._apellido = None
        self._estado = None

    # Setters
    @_id.setter
    def id(self, id):
        self._id = id

    @_nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @_apellido.setter
    def apellido(self, apellido):
        self._apellido = apellido

    @_estado.setter
    def estado(self, estado):
        self._estado = estado

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def estado(self):
        return self._estado