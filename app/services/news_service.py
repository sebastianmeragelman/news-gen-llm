# -------------------------------#
#
# DEFINO LAS FUNCIONES DE SERVICIO PARA GENERAR NOTICIAS
#
# -------------------------------#


from app.scrapers.ddg_scraper import buscador
from app.llm.groq_client import generar_contenido
from app.utils.parser import parsear_json_seguro
from app.utils.logger import logger


def generar_noticia(query: str):
    logger.info(f"Nueva request: {query}")
    
    resultados = buscador(query, 3)
    logger.info(f" Resultados encontrados: {len(resultados)}")

    if not resultados:
        logger.warning("No se encontraron resultados válidos.")
        return {"texto": "", "resumen": ""}

    contexto = "\n\n".join([r["text"] for r in resultados])
    logger.info(f"📄 Contexto generado: {len(contexto)} caracteres")

    try:
        respuesta = generar_contenido(contexto)
        logger.info(" LLM respondió correctamente")
        logger.info(f" RAW LLM OUTPUT:\n{respuesta}")


    except Exception as e:
        logger.error(f" Error LLM: {str(e)}")
        return {
            "texto": "Error generando contenido",
            "resumen": "error-llm"
        }
    data = parsear_json_seguro(respuesta)

    return data