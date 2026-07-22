# =============================================================================
#  modelos/entidad_base.py
#  Clase abstracta que representa una entidad general del sistema.
#
#  Demuestra ABSTRACCIÓN: define un contrato (métodos abstractos) que las
#  clases derivadas están obligadas a implementar, pero no puede instanciarse
#  por sí misma.
# =============================================================================

from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Entidad general de la que heredan Cliente y Servicio."""

    def __init__(self, identificador):
        # Atributo protegido (encapsulación): guion bajo indica uso interno
        self._identificador = identificador

    @property
    def identificador(self):
        """Acceso de solo lectura al identificador de la entidad."""
        return self._identificador

    @abstractmethod
    def obtener_resumen(self):
        """Cada entidad debe devolver un resumen textual de sí misma.

        Es un método abstracto: obliga a las clases hijas a implementarlo.
        """
        raise NotImplementedError
