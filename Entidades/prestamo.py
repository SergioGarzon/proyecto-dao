from datetime import timedelta

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from Entidades.detalle_prestamo import DetallePrestamo
from Entidades.enums import EstadoPrestamo, TipoPrestamo
from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import Base


class Prestamo(Base):
    __tablename__ = "prestamos"

    PLAZO_DIAS = 14

    id_prestamo = Column(Integer, primary_key=True)
    legajo_dni = Column(ForeignKey("socios.legajo_dni"), nullable=False)
    id_sede_origen = Column(ForeignKey("sedes.id_sede"), nullable=False)
    id_sede_destino = Column(ForeignKey("sedes.id_sede"), nullable=False)
    tipo = Column(Enum(TipoPrestamo), nullable=False)
    estado = Column(Enum(EstadoPrestamo), nullable=False, default=EstadoPrestamo.PENDIENTE_ENVIO)
    fecha_prestamo = Column(Date, nullable=False)
    # En un interbibliotecario se fija recién cuando el material llega a destino
    fecha_vencimiento = Column(Date)

    socio = relationship("Socio", back_populates="prestamos")
    sede_origen = relationship("Sede", foreign_keys=[id_sede_origen])
    sede_destino = relationship("Sede", foreign_keys=[id_sede_destino])
    detalles = relationship("DetallePrestamo", back_populates="prestamo", cascade="all, delete-orphan")
    remitos = relationship("Remito", back_populates="prestamo")

    def es_interbibliotecario(self):
        return self.tipo == TipoPrestamo.INTERBIBLIOTECARIO

    def agregar_ejemplar(self, ejemplar):
        if not ejemplar.esta_disponible():
            raise ReglaNegocioError(f"El ejemplar {ejemplar.codigo_inventario} no está disponible.")
        if not ejemplar.pertenece_a(self.sede_origen):
            raise ReglaNegocioError(
                f"El ejemplar {ejemplar.codigo_inventario} no pertenece a la sede {self.sede_origen.nombre}.")
        self.detalles.append(DetallePrestamo(ejemplar=ejemplar, estado_fisico_salida=ejemplar.estado_fisico))

    def validar_sedes(self):
        self.sede_origen.validar_activa()
        self.sede_destino.validar_activa()
        misma_sede = self.sede_origen.id_sede == self.sede_destino.id_sede
        if self.es_interbibliotecario() and misma_sede:
            raise ReglaNegocioError("En un préstamo interbibliotecario las sedes deben ser distintas.")
        if not self.es_interbibliotecario() and not misma_sede:
            raise ReglaNegocioError("En un préstamo local la sede de origen y destino debe ser la misma.")

    def activar(self, hoy):
        self.estado = EstadoPrestamo.ACTIVO
        self.fecha_vencimiento = hoy + timedelta(days=self.PLAZO_DIAS)
        for detalle in self.detalles:
            detalle.ejemplar.marcar_prestado()

    def esta_vencido(self, hoy):
        return self.estado == EstadoPrestamo.ACTIVO and self.fecha_vencimiento < hoy

    def dias_atraso(self, fecha):
        return max(0, (fecha - self.fecha_vencimiento).days)

    def verificar_cierre(self):
        if all(detalle.fue_devuelto() for detalle in self.detalles):
            self.estado = EstadoPrestamo.DEVUELTO

    def marcar_incidencia(self):
        self.estado = EstadoPrestamo.CON_INCIDENCIA
