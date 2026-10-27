from Entidades.estado_socio import EstadoSocio

class Socio:
    
    _legajo_dni = None
    _nombre = None
    _apellido = None
    _fecha_inscripcion = None
    _domicilio_calle = None
    _barrio = None
    _localidad = None
    _estado_socio = None
    
    def __init__(self, nuevo_legajo_dni, nuevo_nombre, nuevo_apellido, nueva_fecha_inscripcion, nuevo_domicilio, nuevo_barrio, nueva_localidad, nuevo_estado):
        self._legajo_dni = nuevo_legajo_dni
        self._nombre = nuevo_nombre
        self._apellido = nuevo_apellido
        self._fecha_inscripcion = nueva_fecha_inscripcion
        self._domicilio_calle = nuevo_domicilio
        self._barrio = nuevo_barrio
        self._localidad = nueva_localidad
        self._estado_socio = EstadoSocio(nuevo_estado)
        
    @property
    def legajo_dni(self):
        return self._legajo_dni

    @property
    def nombre(self):
        return self._nombre
    
    @property
    def apellido(self):
        return self._apellido
    
    @property
    def fecha_inscripcion(self):
        return self._fecha_inscripcion
    
    @property
    def domicilio_calle(self):
        return self._domicilio_calle
    
    @property
    def barrio(self):
        return self._barrio
    
    @property
    def localidad(self):
        return self._localidad
    
    @property
    def estado_socio(self):
        return self._estado_socio
    
    @legajo_dni.setter
    def legajo_dni(self, nuevo_legajo_dni):
        self._legajo_dni = nuevo_legajo_dni
        
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre
    
    @apellido.setter
    def apellido(self, nuevo_apellido):
        self._apellido = nuevo_apellido
        
    @fecha_inscripcion.setter
    def fecha_inscripcion(self, nueva_fecha_inscripcion):
        self._fecha_inscripcion = nueva_fecha_inscripcion
    
    @domicilio_calle.setter
    def domicilio_calle(self, nuevo_domicilio):
        self._domicilio_calle=nuevo_domicilio
    
    @barrio.setter
    def barrio(self, nuevo_barrio):
        self._barrio = nuevo_barrio
        
    @localidad.setter
    def localidad(self, nueva_localidad):
        self._localidad = nueva_localidad
    
    @estado_socio.setter
    def estado_socio(self, nuevo_estado):
        self._estado_socio = nuevo_estado
        
    # Metodo toString en Python, por las dudas lo pongo
        def __str__(self):
            return f'''Socio(Código del socio={self._legajo_dni}, 
                   nombre= {self._nombre},
                   apellido= {self._apellido},
                   fecha de inscripción= {self._fecha_inscripcion},
                   domicilio calle= {self._domicilio_calle},
                   barrio= {self._barrio},
                   localidad= {self._localidad},
                   estado= {self._estado_socio})'''
    
        