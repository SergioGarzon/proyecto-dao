from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Entidades.enums import EstadoEjemplar, EstadoFisico
from Persistencia.conexion import Base


class Ejemplar(Base):
    __tablename__ = "ejemplares"

    id_ejemplar = Column(Integer, primary_key=True)
    codigo_inventario = Column(String(30), nullable=False, unique=True)
    codigo_libro = Column(ForeignKey("libros.codigo_libro"), nullable=False)
    # Sede propietaria: no cambia aunque el ejemplar esté viajando
    id_sede = Column(ForeignKey("sedes.id_sede"), nullable=False)
    estado = Column(Enum(EstadoEjemplar), nullable=False, default=EstadoEjemplar.DISPONIBLE)
    estado_fisico = Column(Enum(EstadoFisico), nullable=False, default=EstadoFisico.BUENO)

    libro = relationship("Libro", back_populates="ejemplares")
    sede = relationship("Sede", back_populates="ejemplares")

    def esta_disponible(self):
        return self.estado == EstadoEjemplar.DISPONIBLE

    def pertenece_a(self, sede):
        return self.id_sede == sede.id_sede

    def preparar_envio(self):
        self.estado = EstadoEjemplar.EN_PREPARACION

    def marcar_en_transito(self):
        self.estado = EstadoEjemplar.EN_TRANSITO

    def marcar_prestado(self):
        self.estado = EstadoEjemplar.PRESTADO

    def marcar_reservado(self):
        self.estado = EstadoEjemplar.RESERVADO

    def recibir_devolucion(self, fisico, requiere_retorno):
        self.estado_fisico = fisico
        if fisico in (EstadoFisico.DESTRUIDO, EstadoFisico.EXTRAVIADO):
            self.estado = EstadoEjemplar.BAJA
        elif requiere_retorno:
            self.preparar_envio()
        else:
            self.finalizar_retorno()

    def finalizar_retorno(self):
        en_condiciones = self.estado_fisico in (EstadoFisico.BUENO, EstadoFisico.REGULAR)
        self.estado = EstadoEjemplar.DISPONIBLE if en_condiciones else EstadoEjemplar.EN_REPARACION

    def registrar_incidencia(self, fisico):
        self.estado_fisico = fisico
        self.estado = EstadoEjemplar.BAJA if fisico == EstadoFisico.EXTRAVIADO else EstadoEjemplar.EN_REPARACION

    def __str__(self):
        return f"{self.codigo_inventario}"
