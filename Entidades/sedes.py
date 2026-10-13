class Sedes:
    _direccion = None
    _contacto = None
    _horarios = None
    _estado = None

    def __init__(self, direccion, contacto, horarios, estado):
        self._direccion = direccion
        self._contacto = contacto
        self._horarios = horarios
        self._estado = estado

        #Setters
    @_direccion.setter
    def direccion(self, direccion):
        self._direccion = direccion

    @_contacto.setter
    def contacto(self, contacto):
        self._contacto = contacto

    @_horarios.setter
    def horarios(self, horarios):
        self._horarios = horarios

    @_estado.setter
    def estado(self, estado):
        self._estado = estado

    # Getters
    @property
    def direccion(self):
        return self._direccion

    @property
    def contacto(self):
        return self._contacto

    @property
    def horarios(self):
        return self._horarios

    @property
    def estado(self):
        return self._estado