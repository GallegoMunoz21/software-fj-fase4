# =============================================================================
#  utils/logger.py
#  Configura el registro (logging) del sistema en un archivo de logs.
#
#  Cada error o evento relevante se guarda en 'logs/sistema.log' con fecha,
#  hora, nivel (INFO / WARNING / ERROR) y mensaje. Esto cumple el requisito
#  de mantener un archivo de logs sin usar base de datos.
# =============================================================================

import logging
import os

# Ruta absoluta a la carpeta 'logs' (junto a la raíz del proyecto)
_CARPETA_LOGS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
_ARCHIVO_LOG = os.path.join(_CARPETA_LOGS, "sistema.log")


def obtener_logger():
    """Crea (o reutiliza) el logger del sistema que escribe en archivo."""
    # Nos aseguramos de que exista la carpeta de logs
    os.makedirs(_CARPETA_LOGS, exist_ok=True)

    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    # Evita agregar el manejador varias veces si se llama repetidamente
    if not logger.handlers:
        manejador = logging.FileHandler(_ARCHIVO_LOG, mode="a", encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        manejador.setFormatter(formato)
        logger.addHandler(manejador)

    return logger
