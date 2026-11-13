from abc import ABC, abstractmethod

from Entidades.enums import EstadoFisico, TipoRemito
from Entidades.excepciones import ReglaNegocioError, TransicionInvalidaError


class EstadoRemito(ABC):
    """Estado del patrón State: por defecto toda operación es una transición inválida."""

    @property
    @abstractmethod
    def nombre(self):
        pass

    def entrar(self, remito):
        pass

    def _rechazar(self, accion):
        raise TransicionInvalidaError(f"No se puede {accion} un remito en estado {self.nombre}.")

    def despachar(self, remito):
        self._rechazar("despachar")

    def iniciar_transito(self, remito):
        self._rechazar("poner en tránsito")

    def recibir(self, remito):
        self._rechazar("recibir")

    def reportar_danio(self, remito):
        self._rechazar("reportar daño en")

    def reportar_extravio(self, remito):
        self._rechazar("reportar extravío de")

    def cancelar(self, remito):
        self._rechazar("cancelar")


class Preparado(EstadoRemito):
    nombre = "Preparado"

    def despachar(self, remito):
        remito.sede_origen.validar_activa()
        remito.sede_destino.validar_activa()
        remito.cambiar_estado(Despachado())

    def cancelar(self, remito):
        if remito.tipo == TipoRemito.RETORNO:
            raise ReglaNegocioError("Un remito de retorno no se puede cancelar: el material tiene que volver.")
        remito.cambiar_estado(Cancelado())


class Despachado(EstadoRemito):
    nombre = "Despachado"

    def iniciar_transito(self, remito):
        remito.cambiar_estado(EnTransito())

    def reportar_extravio(self, remito):
        remito.cambiar_estado(Extraviado())


class EnTransito(EstadoRemito):
    nombre = "EnTransito"

    def entrar(self, remito):
        for ejemplar in remito.ejemplares:
            ejemplar.marcar_en_transito()

    def recibir(self, remito):
        remito.sede_destino.validar_activa()
        remito.cambiar_estado(Recibido())

    def reportar_danio(self, remito):
        remito.cambiar_estado(Danado())

    def reportar_extravio(self, remito):
        remito.cambiar_estado(Extraviado())


class Recibido(EstadoRemito):
    nombre = "Recibido"

    def entrar(self, remito):
        if remito.tipo == TipoRemito.IDA:
            remito.prestamo.activar(remito.fecha_ultimo_cambio())
        else:
            for ejemplar in remito.ejemplares:
                ejemplar.finalizar_retorno()


class Danado(EstadoRemito):
    nombre = "Danado"

    def entrar(self, remito):
        remito.registrar_incidencia(EstadoFisico.DANADO)


class Extraviado(EstadoRemito):
    nombre = "Extraviado"

    def entrar(self, remito):
        remito.registrar_incidencia(EstadoFisico.EXTRAVIADO)


class Cancelado(EstadoRemito):
    """El envío no llegó a salir: los ejemplares vuelven a estar disponibles y el préstamo se cancela."""
    nombre = "Cancelado"

    def entrar(self, remito):
        for ejemplar in remito.ejemplares:
            ejemplar.finalizar_retorno()
        remito.prestamo.cancelar()


ESTADOS_REMITO = {estado.nombre: estado for estado in
                  (Preparado, Despachado, EnTransito, Recibido, Danado, Extraviado, Cancelado)}

ESTADOS_ABIERTOS = (Preparado.nombre, Despachado.nombre, EnTransito.nombre)
# Remitos que terminaron un recorrido real. Cancelado queda afuera: nunca salió, no cuenta en la tasa de envíos
ESTADOS_FINALES = (Recibido.nombre, Danado.nombre, Extraviado.nombre)
