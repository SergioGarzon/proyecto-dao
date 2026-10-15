from estado_sede import EstadoSede

class Sede:
    
    _codigo_sede = None
    _direccion_calle_altura = None
    _barrio = None
    _localidad = None
    _telefono = None
    _email = None
    _hora_apertura = None  # Documentacion https://docs.python.org/es/3.8/library/datetime.html 
    _hora_cierre = None    # Para el tipo de dato "datetime.time"
    _estado = None
    
    def __init__(self, nuevo_codigo, nueva_direccion, nuevo_barrio, nueva_localidad, nuevo_telefono, nuevo_email, nuevo_hora_apertura, nuevo_hora_fin, nuevo_estado_sede):
        self._codigo_sede = nuevo_codigo
        self._direccion_calle_altura = nueva_direccion
        self._barrio = nuevo_barrio
        self._localidad = nueva_localidad
        self._telefono = nuevo_telefono
        self._email = nuevo_email
        self._hora_apertura = nuevo_hora_apertura
        self._hora_cierre = nuevo_hora_fin
        self._estado = EstadoSede(nuevo_estado_sede)
        
    # Getter
    @property
    def codigo_sede(self):
        return self._codigo_sede

    @property
    def direccion_calle_altura(self):
        return self._direccion_calle_altura
    
    @property
    def barrio(self):
        return self._barrio
    
    @property
    def localidad(self):
        return self._localidad
    
    @property
    def telefono(self):
        return self._telefono
    
    @property
    def email(self):
        return self._email
    
    @property
    def hora_apertura(self):
        return self._hora_apertura
    
    @property
    def hora_cierre(self):
        return self._hora_cierre

    @property
    def estado(self):
        return self._estado
    
    # Setter
    @codigo_sede.setter
    def codigo_sede(self, nuevo_codigo):
        self._codigo_sede = nuevo_codigo
        
    @direccion_calle_altura.setter
    def direccion_calle_altura(self, nueva_direccion):
        self._direccion_calle_altura = nueva_direccion
        
    @barrio.setter
    def barrio(self, nuevo_barrio):
        self._barrio = nuevo_barrio
        
    @localidad.setter
    def localidad(self, nueva_localidad):
        self._localidad = nueva_localidad
        
    @telefono.setter
    def telefono(self, nuevo_telefono):
        self._telefono = nuevo_telefono
        
    @email.setter
    def email(self, nuevo_email):
        self._email = nuevo_email
        
    @hora_apertura.setter
    def hora_apertura(self, nuevo_hora_apertura):
        self._hora_apertura = nuevo_hora_apertura
        
    @hora_cierre.setter
    def hora_cierre(self, nuevo_hora_fin):
        self._hora_cierre = nuevo_hora_fin
    
    @estado.setter
    def estado(self, nuevo_estado_sede):
        self._estado = nuevo_estado_sede
                
    # Metodo toString en Python
    def __str__(self):
        return f'''Sede (Codigo de sede = {self._codigo_sede}, direccion= {self._direccion_calle_altura}, 
                barrio= {self._barrio}, localidad= {self._localidad}, telefono= {self._telefono},
                email= {self._email}, hora de apertura= {self._hora_apertura}, hora de cierre= {self._hora_cierre},
                estado= {self._estado})'''
    
    
    
    