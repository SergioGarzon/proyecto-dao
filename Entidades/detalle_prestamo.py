class DetallePrestamo:
    def __init__(self, libro, estado_material = None):
        self.libro = libro
        self.estado_material = estado_material

    @property
    def libro(self):
        return self._libro

    @property
    def estado_material(self):
        return self._estado_material

    @libro.setter
    def libro(self, nuevo_libro):
        self._libro = nuevo_libro

    @estado_material.setter
    def estado_material(self, nuevo_estado_material):
        self._estado_material = nuevo_estado_material
