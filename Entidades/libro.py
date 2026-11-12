from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from Entidades.enums import EstadoEjemplar
from Persistencia.conexion import Base


class Libro(Base):
    __tablename__ = "libros"

    codigo_libro = Column(Integer, primary_key=True)
    isbn = Column(String(20), nullable=False, unique=True)
    titulo = Column(String(150), nullable=False)
    autor = Column(String(100), nullable=False)
    editorial = Column(String(100))
    anio_publicacion = Column(Integer)

    ejemplares = relationship("Ejemplar", back_populates="libro")
    reservas = relationship("Reserva", back_populates="libro")

    def ejemplares_disponibles(self, id_sede=None):
        return [ejemplar for ejemplar in self.ejemplares
                if ejemplar.esta_disponible() and id_sede in (None, ejemplar.id_sede)]

    def disponibilidad_por_sede(self):
        """Devuelve [(sede, disponibles, total)] de las sedes activas que tienen ejemplares de este libro."""
        conteo = {}
        for ejemplar in self.ejemplares:
            if ejemplar.estado == EstadoEjemplar.BAJA or not ejemplar.sede.esta_activa():
                continue
            disponibles, total = conteo.get(ejemplar.sede, (0, 0))
            conteo[ejemplar.sede] = (disponibles + ejemplar.esta_disponible(), total + 1)
        return sorted(((sede, disponibles, total) for sede, (disponibles, total) in conteo.items()),
                      key=lambda fila: fila[0].nombre)

    def __str__(self):
        return f"{self.titulo} ({self.autor})"
