# =============================================================================
#  excepciones.py
#  Excepciones personalizadas del sistema Software FJ.
#
#  Todas heredan de una excepción base común (SoftwareFJError). Esto permite,
#  si se desea, capturar cualquier error propio del sistema con un solo except,
#  y a la vez distinguir cada tipo de error de forma específica.
# =============================================================================


class SoftwareFJError(Exception):
    """Clase base de todas las excepciones propias del sistema."""
    pass


class ErrorValidacionCliente(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""
    pass


class ParametroInvalidoError(SoftwareFJError):
    """Se lanza cuando falta un parámetro o su valor no es válido."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio no disponible."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede confirmarse o procesarse."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce un resultado inválido."""
    pass
