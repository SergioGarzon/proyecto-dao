from datetime import date


class Libro:

    # Esta parte en Python no es necesaria, pero si en la materia lo ponemos asi, lo dejamos entonces
    _codigo_libro = None
    _titulo = None
    _autor = None
    _editorial = None
    _anio_publicacion = None

    def __init__(self, codigo_libro, titulo, autor, editorial, anio_publicacion):
        # El codigo se asigna una sola vez: es el identificador del libro (solo lectura)
        if not str(codigo_libro).strip():
            raise ValueError("El código del libro no puede estar vacío")
        self._codigo_libro = codigo_libro

        # Se usan los setters para que las validaciones se apliquen tambien al crear el objeto
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.anio_publicacion = anio_publicacion

    # Codigo (solo getter, no se modifica)
    @property
    def codigo_libro(self):
        return self._codigo_libro

    # Titulo
    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = self._validar_texto(titulo, "título")

    # Autor
    @property
    def autor(self):
        return self._autor

    @autor.setter
    def autor(self, autor):
        self._autor = self._validar_texto(autor, "autor")

    # Editorial
    @property
    def editorial(self):
        return self._editorial

    @editorial.setter
    def editorial(self, editorial):
        self._editorial = self._validar_texto(editorial, "editorial")

    # Año de publicacion
    @property
    def anio_publicacion(self):
        return self._anio_publicacion

    @anio_publicacion.setter
    def anio_publicacion(self, anio_publicacion):
        if not isinstance(anio_publicacion, int) or isinstance(anio_publicacion, bool):
            raise ValueError("El año de publicación debe ser un número entero")
        if anio_publicacion <= 0 or anio_publicacion > date.today().year:
            raise ValueError("El año de publicación no es válido")
        self._anio_publicacion = anio_publicacion

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacío")
        return valor.strip()

    def __str__(self):
        return f"{self._titulo} - {self._autor} ({self._anio_publicacion})"

    def __repr__(self):
        return f"Libro(codigo_libro={self._codigo_libro!r}, titulo={self._titulo!r})"
