class Libro:
    
    # Esta parte en Python no es necesaria, pero si en la materia lo ponemos asi, lo dejamos entonces
    _codigo_libro = None
    _titulo = None
    _autor = None
    _editorial = None
    _anio_publicacion = None
    
    def __init__(self, codigo_libro_dato, titulo_dato, autor_dato, editorial_dato, anio_publicacion_dato):
        self._codigo_libro = codigo_libro_dato
        self._titulo = titulo_dato
        self._autor = autor_dato
        self._editorial = editorial_dato
        self._anio_publicacion = anio_publicacion_dato
    
    # Setters
    @_codigo_libro.setter
    def codigo_libro(self, codigo_libro_dato):
        self._codigo_libro = codigo_libro_dato
        
    @_titulo.setter
    def titulo(self, titulo_dato):
        self._titulo = titulo_dato
    
    @_autor.setter
    def autor(self, autor_dato):
        self._autor = autor_dato
        
    @_editorial.setter
    def editorial(self, editorial_dato):
        self._editorial = editorial_dato
        
    @_anio_publicacion.setter
    def anio_publicacion(self, anio_publicacion):
        self._anio_publicacion = anio_publicacion
    
    # Getters
    @property
    def Codigo_libro(self):
        return self._codigo_libro
    
    @property
    def Titulo(self):
        return self._titulo
    
    @property
    def Autor(self):
        return self._autor
        
    @property
    def Editorial(self):
        return self._editorial
    
    @property
    def Anio_publicacion(self):
        return self._anio_publicacion
    
    # Metodo toString en Python, por las dudas lo pongo
    def __str__(self):
        return f'''Libro(Código del libro={self._codigo_libro}, 
                Titulo={self._titulo}, 
                Autor={self._autor},
                Editorial={self._editorial},
                Año de publicacion={self._anio_publicacion})'''