class Ejemplar:
    def __init__(self, id_ejemplar, libro, sede, estado):
        self.id_ejemplar = id_ejemplar
        self.libro = libro
        self.sede = sede
        self.estado = estado

    @property
    def id_ejemplar(self):
        return self._id_ejemplar

    @property
    def libro(self):
        return self._libro

    @property
    def sede(self):
        return self._sede

    @property
    def estado(self):
        return self._estado

    @id_ejemplar.setter
    def id_ejemplar(self, nuevo_id_ejemplar):
        self._id_ejemplar = nuevo_id_ejemplar

    @libro.setter
    def libro(self, nuevo_libro):
        self._libro = nuevo_libro

    @sede.setter
    def sede(self, nueva_sede):
        self._sede = nueva_sede

    @estado.setter
    def estado(self, nuevo_estado):
        self._estado = nuevo_estado

    def __str__(self):
        return f"Ejemplar(id={self._id_ejemplar}, libro={self._libro}, sede={self._sede}, estado={self._estado})"
