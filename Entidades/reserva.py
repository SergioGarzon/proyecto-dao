from datetime import timedelta

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from Entidades.enums import EstadoReserva
from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import Base


class Reserva(Base):
    __tablename__ = "reservas"

    DIAS_RETIRO = 3

    id_reserva = Column(Integer, primary_key=True)
    legajo_dni = Column(ForeignKey("socios.legajo_dni"), nullable=False)
    codigo_libro = Column(ForeignKey("libros.codigo_libro"), nullable=False)
    id_sede_retiro = Column(ForeignKey("sedes.id_sede"), nullable=False)
    id_ejemplar = Column(ForeignKey("ejemplares.id_ejemplar"))
    fecha_reserva = Column(Date, nullable=False)
    fecha_expiracion = Column(Date)
    estado = Column(Enum(EstadoReserva), nullable=False, default=EstadoReserva.PENDIENTE)

    socio = relationship("Socio", back_populates="reservas")
    libro = relationship("Libro", back_populates="reservas")
    sede_retiro = relationship("Sede")
    ejemplar = relationship("Ejemplar")

    def esta_vigente(self):
        return self.estado in (EstadoReserva.PENDIENTE, EstadoReserva.ASIGNADA)

    def asignar_ejemplar(self, ejemplar, hoy):
        if self.estado != EstadoReserva.PENDIENTE:
            raise ReglaNegocioError(f"La reserva {self.id_reserva} no está pendiente.")
        self.ejemplar = ejemplar
        self.fecha_expiracion = hoy + timedelta(days=self.DIAS_RETIRO)
        self.estado = EstadoReserva.ASIGNADA
        ejemplar.marcar_reservado()

    def cumplir(self):
        if self.estado != EstadoReserva.ASIGNADA:
            raise ReglaNegocioError(f"La reserva {self.id_reserva} no tiene un ejemplar asignado.")
        self.estado = EstadoReserva.CUMPLIDA
        self._liberar_ejemplar()

    def cancelar(self):
        if not self.esta_vigente():
            raise ReglaNegocioError(f"La reserva {self.id_reserva} ya no está vigente.")
        self.estado = EstadoReserva.CANCELADA
        self._liberar_ejemplar()

    def vencer(self, hoy):
        if self.estado == EstadoReserva.ASIGNADA and self.fecha_expiracion < hoy:
            self.estado = EstadoReserva.VENCIDA
            self._liberar_ejemplar()

    def _liberar_ejemplar(self):
        if self.ejemplar is not None:
            self.ejemplar.finalizar_retorno()
