from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

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

    def cantidad_disponible(self, id_sede=None):
        return len(self.ejemplares_disponibles(id_sede))

    def __str__(self):
        return f"{self.titulo} ({self.autor})"
