from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Persistencia.conexion import Base


class HistorialEstadoRemito(Base):
    __tablename__ = "historial_estados_remito"

    id_historial = Column(Integer, primary_key=True)
    id_remito = Column(ForeignKey("remitos.id_remito"), nullable=False)
    estado_anterior = Column(String(20))
    estado_nuevo = Column(String(20), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    observacion = Column(String(200))

    remito = relationship("Remito", back_populates="historial")
