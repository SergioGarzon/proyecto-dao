class EstadoSede:
    
    _estado_sede = None
    
    def __init__(self, nuevo_estado):
        self._estado_sede = nuevo_estado
    
    # Getter
    @property
    def estado_sede(self):
        return self._estado_sede
    
    # Setter
    @estado_sede.setter
    def estado_sede(self, nuevo_estado):
        self._estado_sede = nuevo_estado
            
    # Metodo toString en Python
    def __str__(self):
        return f", Estado (estado sede = {self._estado_sede} )"