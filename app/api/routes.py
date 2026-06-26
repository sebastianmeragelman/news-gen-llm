
# -------------------------------#
#
# DESCRIPCIÓN: Este archivo define las rutas de la API para generar noticias.
#
# -------------------------------#


from fastapi import APIRouter
from app.models.schemas import QueryInput, NoticiaOutput
from app.services.news_service import generar_noticia
from app.services.image_generation import obtener_imagenes

router = APIRouter()

@router.post("/generar-noticia", response_model=NoticiaOutput)
def generar(data: QueryInput):
    return generar_noticia(data.query)


@router.post("/imagenes")
def imagenes(data: QueryInput):
    return obtener_imagenes(data.query)