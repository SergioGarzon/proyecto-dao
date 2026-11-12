from sqlalchemy import or_
from sqlalchemy.orm import aliased

from Entidades.detalle_prestamo import DetallePrestamo
from Entidades.ejemplar import Ejemplar
from Entidades.enums import EstadoPrestamo
from Entidades.libro import Libro
from Entidades.prestamo import Prestamo
from Entidades.sede import Sede
from Entidades.socio import Socio
from Persistencia.base_dao import BaseDAO


class PrestamoDAO(BaseDAO):

    def __init__(self, session):
        super().__init__(session, Prestamo)

    def listar_recientes(self):
        return self.session.query(Prestamo).order_by(Prestamo.id_prestamo.desc()).all()

    def listar_vencidos(self, hoy):
        return (self.session.query(Prestamo)
                .filter(Prestamo.estado == EstadoPrestamo.ACTIVO, Prestamo.fecha_vencimiento < hoy)
                .order_by(Prestamo.id_prestamo)
                .all())

    def buscar(self, campo, texto):
        """Busca por un solo campo: numero, socio, libro, sede o estado."""
        texto = texto.strip()
        # Escapamos los caracteres de LIKE para que % y _ se busquen como texto
        patron = "%" + texto.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        consulta = self.session.query(Prestamo)

        if campo == "numero":
            consulta = consulta.filter(Prestamo.id_prestamo == int(texto))
        elif campo == "socio":
            condiciones = [Socio.nombre.ilike(patron, escape="\\"), Socio.apellido.ilike(patron, escape="\\")]
            if texto.isdecimal():
                condiciones.append(Socio.legajo_dni == int(texto))
            consulta = consulta.join(Prestamo.socio).filter(or_(*condiciones))
        elif campo == "libro":
            consulta = (consulta.join(Prestamo.detalles).join(DetallePrestamo.ejemplar).join(Ejemplar.libro)
                        .filter(Libro.titulo.ilike(patron, escape="\\"))
                        .distinct())
        elif campo == "sede":
            origen, destino = aliased(Sede), aliased(Sede)
            consulta = (consulta.join(origen, Prestamo.sede_origen).join(destino, Prestamo.sede_destino)
                        .filter(or_(origen.nombre.ilike(patron, escape="\\"),
                                    destino.nombre.ilike(patron, escape="\\"))))
        elif campo == "estado":
            # El texto se compara con lo que ve el usuario ("Activo", "Pendiente de envío"...)
            estados = [estado for estado in EstadoPrestamo if texto.lower() in estado.value.lower()]
            consulta = consulta.filter(Prestamo.estado.in_(estados))
        else:
            raise ValueError(f"Campo de búsqueda desconocido: {campo}")

        return consulta.order_by(Prestamo.id_prestamo.desc()).all()
