# -------------------------------#
#
# DEFINO LAS FUNCIONES DE SERVICIO PARA GENERAR NOTICIAS
#
# -------------------------------#


#from app.scrapers.ddg_scraper import buscador
from app.llm.groq_client import generar_contenido
from app.utils.parser import parsear_json_seguro
from app.scrapers.news_scraper import get_news_context
from app.utils.logger import logger


def generar_noticia(query: str):

    logger.info(f"🚀 Nueva request: {query}")

    textos = get_news_context(query, n=3)
    print("TEXTOS EXTRAIDOS:\n", textos)


    if not textos:
        logger.warning("⚠️ No hay contexto")
        return {
            "texto": "No se encontró información suficiente.",
            "resumen": "sin-datos"
        }

    contexto = "\n\n".join(textos)

    logger.info(f"📄 Contexto generado: {len(contexto)} caracteres")

    # Llamada al llm
    respuesta = generar_contenido(contexto,query=query)
    logger.info(f"RAW LLM RESPONSE:\n{respuesta}")
    data = parsear_json_seguro(respuesta)

    return data