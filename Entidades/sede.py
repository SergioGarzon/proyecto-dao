from sqlalchemy import Column, Enum, Integer, String, Time
from sqlalchemy.orm import relationship

from Entidades.enums import EstadoSede
from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import Base


class Sede(Base):
    __tablename__ = "sedes"

    id_sede = Column(Integer, primary_key=True)
    nombre = Column(String(60), nullable=False, unique=True)
    direccion_calle_altura = Column(String(100), nullable=False)
    barrio = Column(String(60), nullable=False)
    localidad = Column(String(60), nullable=False)
    telefono = Column(String(30))
    email = Column(String(100))
    hora_apertura = Column(Time, nullable=False)
    hora_cierre = Column(Time, nullable=False)
    estado = Column(Enum(EstadoSede), nullable=False, default=EstadoSede.ACTIVA)

    ejemplares = relationship("Ejemplar", back_populates="sede")

    def esta_activa(self):
        return self.estado == EstadoSede.ACTIVA

    def validar_activa(self):
        if not self.esta_activa():
            raise ReglaNegocioError(f"La sede {self.nombre} está dada de baja.")

    def dar_baja(self):
        self.estado = EstadoSede.BAJA

    def reactivar(self):
        self.estado = EstadoSede.ACTIVA

    def __str__(self):
        return f"{self.id_sede} - {self.nombre}"
