
# -------------------------------#
#
# DESCRIPCIÓN: Este archivo define las rutas de la API para generar noticias.
#
# -------------------------------#


from fastapi import APIRouter
from app.models.schemas import QueryInput, NoticiaOutput,ImagenesInput,NoticiasInput
from app.services.news_service import generar_noticia,generar_notica_html
from app.services.image_generation import obtener_imagenes
from app.services.scraper_noticias import obtener_noticias


router = APIRouter()


# ENDPOINT PARA GENERAR NOTICIA EN TEXTO PLANO
@router.post("/generar-noticia", response_model=NoticiaOutput)
def generar(data: QueryInput):
    return generar_noticia(data.query, data.max_links,data.cant_imagenes)

# ENDPOINT PARA GENERAR LINKS CON IMAGENES
@router.post("/imagenes")
def imagenes(data: ImagenesInput):
    return obtener_imagenes(data.query, data.cantidad)

# ENDPOINT PARA OBTENER LISTADO DE NOTICIAS SCRAPEADAS
@router.post("/scrape-noticias")
def scrape_noticias(data: NoticiasInput):
    return obtener_noticias(data.query,data.max_links)

# ENDPOINT PARA GENERAR NOTICIA EN TEXTO HTML (para WordPress)
@router.post("/noticia-html")
def noticia_html(data: QueryInput):
    return generar_notica_html(data.query, data.max_links, data.cant_imagenes)