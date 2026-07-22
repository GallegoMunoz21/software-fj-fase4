# =============================================================================
#  modelos/servicios.py
#  Clase abstracta Servicio + tres servicios especializados.
#
#  Demuestra:
#   - ABSTRACCIÓN: Servicio define métodos abstractos (calcular_costo,
#     describir, validar_parametros).
#   - HERENCIA: los tres servicios heredan de Servicio.
#   - POLIMORFISMO: cada servicio sobrescribe los métodos con su propia lógica.
#   - SOBRECARGA: calcular_costo() acepta parámetros opcionales (impuesto y
#     descuento) para generar distintas variantes del cálculo.
# =============================================================================

from abc import abstractmethod

from modelos.entidad_base import EntidadBase
from excepciones import ParametroInvalidoError, CalculoInconsistenteError


class Servicio(EntidadBase):
    """Clase abstracta base para todos los servicios de Software FJ."""

    def __init__(self, identificador, nombre, disponible=True):
        super().__init__(identificador)
        self._nombre = nombre
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    # ---------------- SOBRECARGA del cálculo de costo ----------------
    #  Un mismo método admite tres formas de uso mediante parámetros opcionales:
    #     calcular_costo(base)                     -> costo simple
    #     calcular_costo(base, impuesto)           -> agrega impuesto
    #     calcular_costo(base, impuesto, descuento)-> impuesto y descuento
    def calcular_costo(self, base, impuesto=0.0, descuento=0.0):
        # Validación defensiva de los parámetros recibidos
        if base is None:
            raise ParametroInvalidoError("Falta el costo base del servicio.")
        if base < 0 or impuesto < 0 or descuento < 0:
            raise ParametroInvalidoError("Los valores de costo no pueden ser negativos.")

        total = base + (base * impuesto) - (base * descuento)

        if total < 0:
            # El descuento no puede dejar el total en negativo
            raise CalculoInconsistenteError("El cálculo produjo un costo negativo.")
        return round(total, 2)

    # ---------------- Métodos abstractos (los definen las hijas) ----------------
    @abstractmethod
    def describir(self):
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, **kwargs):
        raise NotImplementedError

    def obtener_resumen(self):
        estado = "disponible" if self._disponible else "NO disponible"
        return f"Servicio #{self.identificador} - {self._nombre} ({estado})"


# =============================================================================
#  Servicios especializados (POLIMORFISMO)
# =============================================================================

class ReservaSala(Servicio):
    """Reserva de salas: el costo depende de las horas de uso."""

    TARIFA_HORA = 25000  # pesos por hora

    def describir(self):
        return f"Reserva de sala '{self._nombre}' a ${self.TARIFA_HORA:,}/hora."

    def validar_parametros(self, horas=None, **kwargs):
        if horas is None or horas <= 0:
            raise ParametroInvalidoError("Las horas de reserva deben ser mayores a 0.")
        return True

    def calcular_costo(self, horas=None, impuesto=0.19, descuento=0.0):
        # Sobrescribe validando primero sus parámetros propios (polimorfismo)
        self.validar_parametros(horas=horas)
        base = self.TARIFA_HORA * horas
        return super().calcular_costo(base, impuesto, descuento)


class AlquilerEquipos(Servicio):
    """Alquiler de equipos: el costo depende de la cantidad y los días."""

    TARIFA_DIA = 15000  # pesos por equipo por día

    def describir(self):
        return f"Alquiler de equipos '{self._nombre}' a ${self.TARIFA_DIA:,}/equipo/día."

    def validar_parametros(self, cantidad=None, dias=None, **kwargs):
        if not cantidad or cantidad <= 0:
            raise ParametroInvalidoError("La cantidad de equipos debe ser mayor a 0.")
        if not dias or dias <= 0:
            raise ParametroInvalidoError("Los días de alquiler deben ser mayores a 0.")
        return True

    def calcular_costo(self, cantidad=None, dias=None, impuesto=0.19, descuento=0.0):
        self.validar_parametros(cantidad=cantidad, dias=dias)
        base = self.TARIFA_DIA * cantidad * dias
        return super().calcular_costo(base, impuesto, descuento)


class AsesoriaEspecializada(Servicio):
    """Asesoría especializada: tarifa fija por sesión según el nivel."""

    TARIFAS = {"basico": 80000, "intermedio": 120000, "avanzado": 200000}

    def describir(self):
        niveles = ", ".join(self.TARIFAS.keys())
        return f"Asesoría '{self._nombre}'. Niveles disponibles: {niveles}."

    def validar_parametros(self, nivel=None, **kwargs):
        if nivel not in self.TARIFAS:
            raise ParametroInvalidoError(
                f"Nivel '{nivel}' inválido. Use: {list(self.TARIFAS.keys())}.")
        return True

    def calcular_costo(self, nivel=None, impuesto=0.19, descuento=0.0):
        self.validar_parametros(nivel=nivel)
        base = self.TARIFAS[nivel]
        return super().calcular_costo(base, impuesto, descuento)
