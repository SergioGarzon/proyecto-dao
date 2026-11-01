class DetallePrestamo:
    def __init__(self, ejemplar, estado_material = None):
        self.ejemplar = ejemplar
        self.estado_material = estado_material

    @property
    def ejemplar(self):
        return self._ejemplar

    @property
    def estado_material(self):
        return self._estado_material

    @ejemplar.setter
    def ejemplar(self, nuevo_ejemplar):
        self._ejemplar = nuevo_ejemplar

    @estado_material.setter
    def estado_material(self, nuevo_estado_material):
        self._estado_material = nuevo_estado_material
