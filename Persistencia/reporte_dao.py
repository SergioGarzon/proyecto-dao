"""Consultas de los reportes: agregan en SQL (JOIN, GROUP BY, COUNT, SUM, AVG) y devuelven filas simples."""
from sqlalchemy import case, func
from sqlalchemy.orm import aliased

from Entidades.detalle_prestamo import DetallePrestamo
from Entidades.ejemplar import Ejemplar
from Entidades.enums import EstadoPrestamo, TipoPrestamo
from Entidades.estado_remito import ESTADOS_FINALES, Despachado, Recibido
from Entidades.historial_estado_remito import HistorialEstadoRemito
from Entidades.libro import Libro
from Entidades.multa import Multa
from Entidades.prestamo import Prestamo
from Entidades.remito import Remito
from Entidades.sede import Sede
from Entidades.socio import Socio


class ReporteDAO:

    def __init__(self, session):
        self.session = session

    # Reporte 1: movimiento de ejemplares entre sedes
    def envios_por_ruta(self, desde, hasta):
        """(origen, destino, envíos, recibidos) de los remitos emitidos en el período."""
        origen, destino = aliased(Sede), aliased(Sede)
        recibidos = func.sum(case((Remito.estado == Recibido.nombre, 1), else_=0))
        return (self.session.query(origen.nombre, destino.nombre, func.count(Remito.id_remito), recibidos)
                .join(origen, Remito.sede_origen)
                .join(destino, Remito.sede_destino)
                .filter(Remito.fecha_emision.between(desde, hasta))
                .group_by(origen.nombre, destino.nombre)
                .order_by(func.count(Remito.id_remito).desc(), origen.nombre, destino.nombre)
                .all())

    def transito_promedio_por_ruta(self, desde, hasta):
        """(origen, destino, horas promedio) entre el despacho y la recepción, sacado del historial del remito."""
        origen, destino = aliased(Sede), aliased(Sede)
        despacho, recepcion = aliased(HistorialEstadoRemito), aliased(HistorialEstadoRemito)
        horas = (func.julianday(recepcion.fecha_hora) - func.julianday(despacho.fecha_hora)) * 24
        return (self.session.query(origen.nombre, destino.nombre, func.avg(horas))
                .join(origen, Remito.sede_origen)
                .join(destino, Remito.sede_destino)
                .join(despacho, (despacho.id_remito == Remito.id_remito) & (despacho.estado_nuevo == Despachado.nombre))
                .join(recepcion, (recepcion.id_remito == Remito.id_remito) & (recepcion.estado_nuevo == Recibido.nombre))
                .filter(Remito.fecha_emision.between(desde, hasta))
                .group_by(origen.nombre, destino.nombre)
                .all())

    # Reporte 2: tasa de envíos exitosos e incidencias
    def remitos_finalizados_por_sede(self, desde, hasta):
        """(sede de origen, estado final, cantidad): solo remitos que ya terminaron su recorrido."""
        return (self.session.query(Sede.nombre, Remito.estado, func.count(Remito.id_remito))
                .join(Sede, Remito.sede_origen)
                .filter(Remito.fecha_emision.between(desde, hasta), Remito.estado.in_(ESTADOS_FINALES))
                .group_by(Sede.nombre, Remito.estado)
                .order_by(Sede.nombre)
                .all())

    # Reporte 3: libros más solicitados para préstamos entre sedes
    def libros_mas_pedidos_intersedes(self, desde, hasta, limite):
        """(título, autor, cantidad) de los libros más pedidos en préstamos interbibliotecarios."""
        cantidad = func.count(DetallePrestamo.id_detalle)
        return (self.session.query(Libro.titulo, Libro.autor, cantidad)
                .select_from(Prestamo)
                .join(Prestamo.detalles)
                .join(DetallePrestamo.ejemplar)
                .join(Ejemplar.libro)
                .filter(Prestamo.tipo == TipoPrestamo.INTERBIBLIOTECARIO,
                        Prestamo.fecha_prestamo.between(desde, hasta))
                .group_by(Libro.codigo_libro, Libro.titulo, Libro.autor)
                .order_by(cantidad.desc(), Libro.titulo)
                .limit(limite)
                .all())

    # Reporte 4: préstamos vencidos y multas acumuladas
    def multas_por_mes_y_motivo(self, desde, hasta):
        """(mes AAAA-MM, motivo, cantidad, monto, monto pagado) de las multas generadas en el período."""
        mes = func.strftime("%Y-%m", Multa.fecha_generacion)
        pagado = func.sum(case((Multa.fecha_pago.isnot(None), Multa.monto), else_=0))
        return (self.session.query(mes, Multa.motivo, func.count(Multa.id_multa), func.sum(Multa.monto), pagado)
                .filter(Multa.fecha_generacion.between(desde, hasta))
                .group_by(mes, Multa.motivo)
                .order_by(mes)
                .all())

    def prestamos_vencidos(self, hoy):
        """(id, "Apellido, Nombre", fecha de vencimiento) de los préstamos activos ya vencidos."""
        return (self.session.query(Prestamo.id_prestamo, Socio.apellido + ", " + Socio.nombre,
                                   Prestamo.fecha_vencimiento)
                .join(Prestamo.socio)
                .filter(Prestamo.estado == EstadoPrestamo.ACTIVO, Prestamo.fecha_vencimiento < hoy)
                .order_by(Prestamo.fecha_vencimiento)
                .all())

    def socios_con_mas_deuda(self, limite):
        """(legajo, "Apellido, Nombre", total pendiente) ordenado de mayor a menor deuda."""
        total = func.sum(Multa.monto)
        return (self.session.query(Socio.legajo_dni, Socio.apellido + ", " + Socio.nombre, total)
                .join(Multa.socio)
                .filter(Multa.fecha_pago.is_(None))
                .group_by(Socio.legajo_dni, Socio.apellido, Socio.nombre)
                .order_by(total.desc())
                .limit(limite)
                .all())
