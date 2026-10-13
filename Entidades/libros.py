class Libros:
    
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
        
    # Faltan los setteres de editorial_dato y anio_publicacion_dato    
    
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