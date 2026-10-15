class EstadoSocio:
    
    _estado_socio = None
    
    def __init__(self, nuevo_estado):
        self._estado_socio = nuevo_estado
    
    # Getter
    @property
    def estado_socio(self):
        return self._estado_socio
    
    # Setter
    @estado_socio.setter
    def estado_socio(self, nuevo_estado):
        self._estado_socio = nuevo_estado
            
    # Metodo toString en Python
    def __str__(self):
        return f", Estado (estado socio = {self._estado_socio} )"