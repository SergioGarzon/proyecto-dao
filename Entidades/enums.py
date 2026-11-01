from enum import Enum


class EstadoSede(Enum):
    ACTIVA = "Activa"
    BAJA = "Baja"


class EstadoSocio(Enum):
    ACTIVO = "Activo"
    INHABILITADO = "Inhabilitado"
    BAJA = "Baja"


class EstadoEjemplar(Enum):
    DISPONIBLE = "Disponible"
    RESERVADO = "Reservado"
    EN_PREPARACION = "En preparación"
    EN_TRANSITO = "En tránsito"
    PRESTADO = "Prestado"
    EN_REPARACION = "En reparación"
    BAJA = "Baja"


class EstadoFisico(Enum):
    BUENO = "Bueno"
    REGULAR = "Regular"
    DANADO = "Dañado"
    DESTRUIDO = "Destruido"
    EXTRAVIADO = "Extraviado"


class EstadoPrestamo(Enum):
    PENDIENTE_ENVIO = "Pendiente de envío"
    ACTIVO = "Activo"
    DEVUELTO = "Devuelto"
    CON_INCIDENCIA = "Con incidencia"


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    ASIGNADA = "Asignada"
    CUMPLIDA = "Cumplida"
    CANCELADA = "Cancelada"
    VENCIDA = "Vencida"


class TipoPrestamo(Enum):
    LOCAL = "Local"
    INTERBIBLIOTECARIO = "Interbibliotecario"


class TipoRemito(Enum):
    IDA = "Ida"
    RETORNO = "Retorno"


class MotivoMulta(Enum):
    ATRASO = "Atraso"
    DANIO = "Daño"
    EXTRAVIO = "Extravío"
