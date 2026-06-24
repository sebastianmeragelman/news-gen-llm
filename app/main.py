# -------------------------------#
#
# Inicializa el entry point de la aplicación FastAPI
#
# -------------------------------#

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Generador de Noticias - API")

app.include_router(router)