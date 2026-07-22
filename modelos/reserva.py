# =============================================================================
#  modelos/reserva.py
#  Clase Reserva: integra cliente, servicio, duración y estado.
#
#  Demuestra los distintos patrones de manejo de excepciones:
#   - try/except/else   (en confirmar)
#   - try/except/finally (en procesar)
#   - encadenamiento de excepciones con 'raise ... from ...'
# =============================================================================

from excepciones import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)
from utils.logger import obtener_logger

log = obtener_logger()


class Reserva:
    """Representa una reserva que une a un cliente con un servicio."""

    def __init__(self, numero, cliente, servicio, duracion, **parametros):
        self.numero = numero
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion          # horas / días / sesiones según el servicio
        self.parametros = parametros      # parámetros propios del cálculo
        self.estado = "pendiente"
        self.costo = None

    # ---------------- Confirmación: try / except / else ----------------
    def confirmar(self):
        """Confirma la reserva solo si el servicio está disponible."""
        try:
            if not self.servicio.disponible:
                # Se lanza una excepción personalizada
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre}' no está disponible.")
        except ServicioNoDisponibleError as e:
            self.estado = "rechazada"
            log.error(f"Reserva #{self.numero} rechazada: {e}")
            raise  # se relanza para que el llamador se entere
        else:
            # El bloque 'else' corre SOLO si no hubo excepción
            self.estado = "confirmada"
            log.info(f"Reserva #{self.numero} confirmada para "
                     f"{self.cliente.obtener_resumen()}")
            return True

    # ---------------- Procesamiento: try / except / finally + encadenamiento ---
    def procesar(self):
        """Calcula el costo de la reserva y registra el cierre de la operación."""
        if self.estado != "confirmada":
            raise ReservaInvalidaError(
                f"No se puede procesar la reserva #{self.numero} en estado "
                f"'{self.estado}'.")
        try:
            # Cada servicio calcula su costo de forma distinta (polimorfismo)
            self.costo = self.servicio.calcular_costo(**self.parametros)
        except ZeroDivisionError as e:
            # Encadenamiento: se conserva la causa original con 'from e'
            raise CalculoInconsistenteError(
                f"Error de cálculo en la reserva #{self.numero}.") from e
        else:
            self.estado = "procesada"
            log.info(f"Reserva #{self.numero} procesada. Costo: ${self.costo:,.2f}")
            return self.costo
        finally:
            # El bloque 'finally' SIEMPRE se ejecuta (haya error o no)
            log.info(f"Fin del procesamiento de la reserva #{self.numero} "
                     f"(estado actual: {self.estado}).")

    # ---------------- Cancelación ----------------
    def cancelar(self):
        self.estado = "cancelada"
        log.info(f"Reserva #{self.numero} cancelada.")
        return True

    def __str__(self):
        costo = f"${self.costo:,.2f}" if self.costo is not None else "sin calcular"
        return (f"Reserva #{self.numero} | {self.cliente.nombre} -> "
                f"{self.servicio.nombre} | estado: {self.estado} | costo: {costo}")
