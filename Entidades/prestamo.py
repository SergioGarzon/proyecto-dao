from Entidades.detalle_prestamo import DetallePrestamo

class Prestamo:
    def __init__(self, id_prestamo, socio, sede_origen, sede_destino, tipo, fecha_prestamo, fecha_devolucion, estado):
        self.id_prestamo = id_prestamo
        self.socio = socio
        self.detalle_prestamo = []
        self.sede_origen = sede_origen
        self.sede_destino = sede_destino
        self.tipo = tipo
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado

    def agregar_detalle(self, ejemplar):
        self.detalle_prestamo.append(DetallePrestamo(ejemplar))
    
    @property
    def id_prestamo(self): 
        return self._id_prestamo

    @property
    def socio(self):
        return self._socio

    @property
    def detalle_prestamo(self):
        return self._detalle_prestamo

    @property
    def fecha_prestamo(self):
        return self._fecha_prestamo

    @property
    def fecha_devolucion(self):
        return self._fecha_devolucion

    @property
    def sede_origen(self):
        return self._sede_origen

    @property
    def sede_destino(self):
        return self._sede_destino

    @property
    def tipo(self):
        return self._tipo

    @property
    def estado(self):
        return self._estado


    @id_prestamo.setter
    def id_prestamo(self, nuevo_id_prestamo):
        self._id_prestamo = nuevo_id_prestamo

    @socio.setter
    def socio(self, nuevo_socio):
        self._socio = nuevo_socio

    @detalle_prestamo.setter
    def detalle_prestamo(self, nuevo_detalle_prestamo):
        self._detalle_prestamo = nuevo_detalle_prestamo

    @fecha_prestamo.setter
    def fecha_prestamo(self, nueva_fecha_prestamo):
        self._fecha_prestamo = nueva_fecha_prestamo

    @fecha_devolucion.setter
    def fecha_devolucion(self, nueva_fecha_devolucion):
        self._fecha_devolucion = nueva_fecha_devolucion

    @sede_origen.setter
    def sede_origen(self, nueva_sede_origen):
        self._sede_origen = nueva_sede_origen

    @sede_destino.setter
    def sede_destino(self, nueva_sede_destino):
        self._sede_destino = nueva_sede_destino

    @tipo.setter
    def tipo(self, nuevo_tipo):
        self._tipo = nuevo_tipo

    @estado.setter
    def estado(self, nuevo_estado):
        self._estado = nuevo_estado