from Entidades.estado_libro import EstadoLibro

class Libro:
    
    # Esta parte en Python no es necesaria, pero si en la materia lo ponemos asi, lo dejamos entonces
    _codigo_libro = None
    _titulo = None
    _autor = None
    _editorial = None
    _anio_publicacion = None
    _estado_libro = None
    
    def __init__(self, nuevo_codigo, nuevo_titulo, nuevo_autor, nuevo_editorial, nuevo_anio_publicacion, nuevo_estado):
        self._codigo_libro = nuevo_codigo
        self._titulo = nuevo_titulo
        self._autor = nuevo_autor
        self._editorial = nuevo_editorial
        self._anio_publicacion = nuevo_anio_publicacion
        self._estado_libro = EstadoLibro(nuevo_estado)
    
    # Getters
    @property
    def codigo_libro(self):
        return self._codigo_libro
        
    @property
    def titulo(self):
        return self._titulo
        
    @property
    def autor(self):
        return self._autor
            
    @property
    def editorial(self):
        return self._editorial
        
    @property
    def anio_publicacion(self):
        return self._anio_publicacion
    
    @property
    def estado_libro(self):
        return self._estado_libro   
    
    # Setters
    @codigo_libro.setter
    def codigo_libro(self, nuevo_codigo):
        self._codigo_libro = nuevo_codigo
        
    @titulo.setter
    def titulo(self, nuevo_titulo):
        self._titulo = nuevo_titulo
    
    @autor.setter
    def autor(self, nuevo_autor):
        self._autor = nuevo_autor
        
    @editorial.setter
    def editorial(self, nuevo_editorial):
        self._editorial = nuevo_editorial
        
    @anio_publicacion.setter
    def anio_publicacion(self, nuevo_anio_publicacion):
        self._anio_publicacion = nuevo_anio_publicacion
        
    @estado_libro.setter
    def estado_libro(self, nuevo_estado):
        self._estado_libro = nuevo_estado
    
    # Metodo toString en Python, por las dudas lo pongo
    def __str__(self):
        return f'''Libro(Código del libro={self._codigo_libro}, 
                Titulo={self._titulo}, 
                Autor={self._autor},
                Editorial={self._editorial},
                Año de publicacion={self._anio_publicacion},
                Estado libro= {self._estado_libro})'''