# =============================================================================
#  modelos/cliente.py
#  Clase Cliente: encapsula los datos personales y los valida de forma robusta.
#
#  Demuestra ENCAPSULACIÓN (atributos protegidos + properties) y validación
#  estricta que lanza excepciones personalizadas cuando los datos son inválidos.
# =============================================================================

import re  # expresiones regulares, para validar el correo

from modelos.entidad_base import EntidadBase
from excepciones import ErrorValidacionCliente


class Cliente(EntidadBase):
    """Representa a un cliente de Software FJ con datos validados."""

    def __init__(self, identificacion, nombre, email):
        # Se reutiliza el constructor del padre para el identificador
        super().__init__(identificacion)
        # Los setters (properties) validan cada dato al asignarlo
        self.nombre = nombre
        self.email = email

    # ---------------- Encapsulación con properties ----------------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        # Validación: el nombre no puede estar vacío ni ser solo espacios
        if not valor or not valor.strip():
            raise ErrorValidacionCliente("El nombre del cliente no puede estar vacío.")
        if len(valor.strip()) < 3:
            raise ErrorValidacionCliente("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        # Validación del formato del correo con una expresión regular simple
        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
        if not valor or not re.match(patron, valor):
            raise ErrorValidacionCliente(f"El email '{valor}' no tiene un formato válido.")
        self._email = valor

    # ---------------- Implementación del método abstracto ----------------
    def obtener_resumen(self):
        return f"Cliente #{self.identificador} - {self._nombre} <{self._email}>"
