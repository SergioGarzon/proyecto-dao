from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from Entidades.enums import EstadoFisico, MotivoMulta
from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import Base


class Multa(Base):
    __tablename__ = "multas"

    MONTO_DIA = 100.0
    MONTO_DANO = 5000.0
    MONTO_EXTRAVIO = 15000.0

    id_multa = Column(Integer, primary_key=True)
    legajo_dni = Column(ForeignKey("socios.legajo_dni"), nullable=False)
    id_detalle = Column(ForeignKey("detalles_prestamo.id_detalle"), nullable=False)
    motivo = Column(Enum(MotivoMulta), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_generacion = Column(Date, nullable=False)
    fecha_pago = Column(Date)

    socio = relationship("Socio", back_populates="multas")
    detalle = relationship("DetallePrestamo")

    @classmethod
    def generar(cls, detalle, fecha):
        socio = detalle.prestamo.socio
        multas = []
        dias = detalle.prestamo.dias_atraso(fecha)
        if dias > 0:
            multas.append(cls(socio=socio, detalle=detalle, motivo=MotivoMulta.ATRASO,
                              monto=dias * cls.MONTO_DIA, fecha_generacion=fecha))
        fisico = detalle.estado_fisico_devolucion
        if fisico == EstadoFisico.DANADO:
            multas.append(cls(socio=socio, detalle=detalle, motivo=MotivoMulta.DANIO,
                              monto=cls.MONTO_DANIO, fecha_generacion=fecha))
        elif fisico in (EstadoFisico.DESTRUIDO, EstadoFisico.EXTRAVIADO):
            multas.append(cls(socio=socio, detalle=detalle, motivo=MotivoMulta.EXTRAVIO,
                              monto=cls.MONTO_EXTRAVIO, fecha_generacion=fecha))
        return multas

    def esta_pendiente(self):
        return self.fecha_pago is None

    def pagar(self, fecha):
        if not self.esta_pendiente():
            raise ReglaNegocioError(f"La multa {self.id_multa} ya está pagada.")
        self.fecha_pago = fecha
