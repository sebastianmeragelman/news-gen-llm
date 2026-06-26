from app.scrapers.image_unsplash import obtener_imagenes_unsplash
from app.models.schemas import ImagenesOutput


def obtener_imagenes(query: str):
    urls = obtener_imagenes_unsplash(query)

    return {
        "query": query,
        "imagenes": urls
    }