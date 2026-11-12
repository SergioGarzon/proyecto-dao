from datetime import date

from sqlalchemy import Column, Date, Enum, Integer, String
from sqlalchemy.orm import relationship

from Entidades.enums import EstadoPrestamo, EstadoSocio
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
        if self.estado == EstadoSocio.BAJA:
            raise ReglaNegocioError(f"El socio {self.legajo_dni} está dado de baja.")
        # La deuda se mira en el momento: así nunca se presta aunque el estado guardado esté desactualizado
        motivo = self.motivo_inhabilitacion(hoy)
        if motivo:
            raise ReglaNegocioError(f"El socio {self.legajo_dni} está inhabilitado: tiene {motivo}.")
        if self.estado == EstadoSocio.INHABILITADO:
            raise ReglaNegocioError(f"El socio {self.legajo_dni} no está habilitado.")

    # Habilitación automática: la decide el negocio (multas y plazos vencidos), nunca el usuario
    def motivo_inhabilitacion(self, hoy):
        if any(prestamo.esta_vencido(hoy) for prestamo in self.prestamos):
            return "préstamos vencidos"
        if self.total_multas_pendientes() > 0:
            return "multas sin pagar"
        return None

    def actualizar_habilitacion(self, hoy):
        """Pasa a Inhabilitado si tiene deuda y vuelve a Activo cuando la salda. Devuelve si cambió."""
        if self.estado == EstadoSocio.BAJA:
            return False
        nuevo = EstadoSocio.INHABILITADO if self.motivo_inhabilitacion(hoy) else EstadoSocio.ACTIVO
        cambio = nuevo != self.estado
        self.estado = nuevo
        return cambio

    # Alta y baja: son decisiones del bibliotecario
    def dar_baja(self):
        if self.estado == EstadoSocio.BAJA:
            raise ReglaNegocioError(f"El socio {self.legajo_dni} ya está dado de baja.")
        if any(prestamo.estado in (EstadoPrestamo.PENDIENTE_ENVIO, EstadoPrestamo.ACTIVO)
               for prestamo in self.prestamos):
            raise ReglaNegocioError(f"No se puede dar de baja al socio {self.legajo_dni}: tiene préstamos sin devolver.")
        if self.total_multas_pendientes() > 0:
            raise ReglaNegocioError(f"No se puede dar de baja al socio {self.legajo_dni}: tiene multas sin pagar.")
        if any(reserva.esta_vigente() for reserva in self.reservas):
            raise ReglaNegocioError(f"No se puede dar de baja al socio {self.legajo_dni}: tiene reservas vigentes.")
        self.estado = EstadoSocio.BAJA

    def dar_alta(self, hoy):
        if self.estado != EstadoSocio.BAJA:
            raise ReglaNegocioError(f"El socio {self.legajo_dni} no está dado de baja.")
        self.estado = EstadoSocio.ACTIVO
        self.actualizar_habilitacion(hoy)

    def total_multas_pendientes(self):
        return sum(multa.monto for multa in self.multas if multa.esta_pendiente())

    def __str__(self):
        return f"{self.legajo_dni} - {self.apellido}, {self.nombre}"
