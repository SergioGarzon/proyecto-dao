from datetime import date

from sqlalchemy import Column, Date, Enum, Integer, String
from sqlalchemy.orm import relationship

from Entidades.enums import EstadoSocio
from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import Base


class Socio(Base):
    __tablename__ = "socios"

    legajo_dni = Column(Integer, primary_key=True, autoincrement=False)
    nombre = Column(String(60), nullable=False)
    apellido = Column(String(60), nullable=False)
    fecha_inscripcion = Column(Date, nullable=False, default=date.today)
    domicilio_calle = Column(String(100), nullable=False)
    barrio = Column(String(60), nullable=False)
    localidad = Column(String(60), nullable=False)
    estado = Column(Enum(EstadoSocio), nullable=False, default=EstadoSocio.ACTIVO)

    prestamos = relationship("Prestamo", back_populates="socio")
    reservas = relationship("Reserva", back_populates="socio")
    multas = relationship("Multa", back_populates="socio")

    def esta_habilitado(self):
        return self.estado == EstadoSocio.ACTIVO

    def validar_habilitado(self, hoy):
        if not self.esta_habilitado():
            raise ReglaNegocioError(f"El socio {self.legajo_dni} no está habilitado.")
        if any(prestamo.esta_vencido(hoy) for prestamo in self.prestamos):
            raise ReglaNegocioError(f"El socio {self.legajo_dni} tiene préstamos vencidos.")
        if self.total_multas_pendientes() > 0:
            raise ReglaNegocioError(f"El socio {self.legajo_dni} tiene multas sin pagar.")

    def inhabilitar(self):
        if self.estado == EstadoSocio.BAJA:
            raise ReglaNegocioError("No se puede inhabilitar un socio dado de baja.")
        self.estado = EstadoSocio.INHABILITADO

    def habilitar(self):
        self.estado = EstadoSocio.ACTIVO

    def dar_baja(self):
        self.estado = EstadoSocio.BAJA

    def total_multas_pendientes(self):
        return sum(multa.monto for multa in self.multas if multa.esta_pendiente())

    def __str__(self):
        return f"{self.legajo_dni} - {self.apellido}, {self.nombre}"
