from datetime import datetime

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from Entidades.enums import TipoRemito
from Entidades.estado_remito import ESTADOS_REMITO, Preparado
from Entidades.historial_estado_remito import HistorialEstadoRemito
from Persistencia.conexion import Base

remito_ejemplares = Table(
    "remito_ejemplares", Base.metadata,
    Column("id_remito", ForeignKey("remitos.id_remito"), primary_key=True),
    Column("id_ejemplar", ForeignKey("ejemplares.id_ejemplar"), primary_key=True))


class Remito(Base):
    """Contexto del patrón State: delega cada operación en su estado actual."""

    __tablename__ = "remitos"

    id_remito = Column(Integer, primary_key=True)
    numero = Column(String(20), nullable=False, unique=True)
    id_prestamo = Column(ForeignKey("prestamos.id_prestamo"), nullable=False)
    id_sede_origen = Column(ForeignKey("sedes.id_sede"), nullable=False)
    id_sede_destino = Column(ForeignKey("sedes.id_sede"), nullable=False)
    tipo = Column(Enum(TipoRemito), nullable=False)
    fecha_emision = Column(Date, nullable=False)
    estado = Column(String(20), nullable=False)

    prestamo = relationship("Prestamo", back_populates="remitos")
    sede_origen = relationship("Sede", foreign_keys=[id_sede_origen])
    sede_destino = relationship("Sede", foreign_keys=[id_sede_destino])
    ejemplares = relationship("Ejemplar", secondary=remito_ejemplares)
    historial = relationship("HistorialEstadoRemito", back_populates="remito", cascade="all, delete-orphan",
                             order_by="HistorialEstadoRemito.id_historial")

    def __init__(self, numero, prestamo, origen, destino, tipo, ejemplares, hoy):
        self.numero = numero
        self.prestamo = prestamo
        self.sede_origen = origen
        self.sede_destino = destino
        self.tipo = tipo
        self.ejemplares = ejemplares
        self.fecha_emision = hoy
        self.cambiar_estado(Preparado())

    @property
    def estado_actual(self):
        # La columna guarda el nombre, así un remito leído de la base sigue funcionando con State
        return ESTADOS_REMITO[self.estado]()

    def cambiar_estado(self, nuevo):
        self.historial.append(HistorialEstadoRemito(estado_anterior=self.estado, estado_nuevo=nuevo.nombre,
                                                    fecha_hora=datetime.now()))
        self.estado = nuevo.nombre
        nuevo.entrar(self)

    def despachar(self):
        self.estado_actual.despachar(self)

    def iniciar_transito(self):
        self.estado_actual.iniciar_transito(self)

    def recibir(self):
        self.estado_actual.recibir(self)

    def reportar_danio(self):
        self.estado_actual.reportar_danio(self)

    def reportar_extravio(self):
        self.estado_actual.reportar_extravio(self)

    def cancelar(self):
        self.estado_actual.cancelar(self)

    def registrar_incidencia(self, fisico):
        for ejemplar in self.ejemplares:
            ejemplar.registrar_incidencia(fisico)
        if self.tipo == TipoRemito.IDA:
            self.prestamo.marcar_incidencia()

    def fecha_ultimo_cambio(self):
        return self.historial[-1].fecha_hora.date()
