class ReglaNegocioError(Exception):
    """Una operación viola una regla del negocio. Las vistas muestran su mensaje."""


class TransicionInvalidaError(ReglaNegocioError):
    """El estado actual del remito no admite la operación pedida."""
