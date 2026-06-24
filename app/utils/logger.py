# ------------------------------------#
#
# UTILIDAD DE LOGGING PARA LA APLICACIÓN
#
# ------------------------------------#


import logging
import sys
from pathlib import Path

#  Ruta base del proyecto (sube desde /app/utils)
BASE_DIR = Path(__file__).resolve().parents[2]

#  carpeta logs fuera de app/
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logger():
    logger = logging.getLogger("news-api")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )

    # consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # archivo
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()