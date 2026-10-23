from sqlalchemy import Column, Integer, String, Date 

class EstadoSocio:
    
    __tablename__ = "estados_socios" # Pongo el nombre de la tabla Estados Socios    
    
    _id_estado_socio = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    _estado_socio = Column(String(20), nullable=False)
    
    
    # Hay que ver bien esto
    socios = relationship('socios', back_populates='estados_socios')
        
    
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