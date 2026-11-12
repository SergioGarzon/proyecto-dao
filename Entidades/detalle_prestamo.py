from sqlalchemy import Column, Date, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from Entidades.enums import EstadoFisico
from Entidades.excepciones import ReglaNegocioError
from Persistencia.conexion import Base


class DetallePrestamo(Base):
    __tablename__ = "detalles_prestamo"

    id_detalle = Column(Integer, primary_key=True)
    id_prestamo = Column(ForeignKey("prestamos.id_prestamo"), nullable=False)
    id_ejemplar = Column(ForeignKey("ejemplares.id_ejemplar"), nullable=False)
    estado_fisico_salida = Column(Enum(EstadoFisico), nullable=False)
    estado_fisico_devolucion = Column(Enum(EstadoFisico))
    fecha_devolucion = Column(Date)

    prestamo = relationship("Prestamo", back_populates="detalles")
    ejemplar = relationship("Ejemplar")

    def fue_devuelto(self):
        return self.fecha_devolucion is not None

    def registrar_devolucion(self, fecha, fisico):
        if self.fue_devuelto():
            raise ReglaNegocioError(f"El ejemplar {self.ejemplar.codigo_inventario} ya fue devuelto.")
        self.fecha_devolucion = fecha
        self.estado_fisico_devolucion = fisico
        vuelve_a_origen = fisico not in (EstadoFisico.DESTRUIDO, EstadoFisico.EXTRAVIADO)
        self.ejemplar.recibir_devolucion(fisico, self.prestamo.es_interbibliotecario() and vuelve_a_origen)