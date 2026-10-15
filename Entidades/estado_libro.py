class EstadoLibro:
    
    _estado_libro = None
    
    def __init__(self, nuevo_estado):
        self._estado_libro = nuevo_estado
    
    # Getter
    @property
    def estado_libro(self):
        return self._estado_libro
    
    # Setter
    @estado_libro.setter
    def estado_libro(self, nuevo_estado):
        self._estado_libro = nuevo_estado
            
    # Metodo toString en Python
    def __str__(self):
        return f", Estado (estado libro = {self._estado_libro} )"