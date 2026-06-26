# -------------------------------#
#
# DEFINO LAS FUNCIONES DE SERVICIO PARA GENERAR NOTICIAS
#
# -------------------------------#



from app.llm.groq_client import generar_contenido, filtrar_contenido
from app.utils.parser import parsear_json_seguro, limpiar_json_string
from app.scrapers.news_scraper import get_news_context
from app.utils.logger import logger
import json

def generar_noticia(query: str):

    logger.info(f"🚀 Nueva request: {query}")

    
    
    noticias = get_news_context(query, n=30)

    

    logger.info(f"📄 Contexto generado: {len(noticias)} elementos")

    # Llamada al llm

    top_noticias = filtrar_contenido(noticias,query)
    top_noticias = top_noticias.get('noticias')
    print("##################################")
    print(" ------ LOG top_noticias post filtrar_contenido------")
    print(top_noticias)
    print(" -------------------------------")
    #if type(top_noticias) is not list:
    
    #    top_noticias = limpiar_json_string(top_noticias)
    #    print("##################################")
    #    print(" ------ LOG top_noticias post limpiar_json_string------")
    #    print(top_noticias)
    #    print(" -------------------------------")
    #else:
    #    top_noticias = str(top_noticias)
    #top_noticias = json.loads(top_noticias)
    
        
    if not top_noticias:
        logger.warning("⚠️ No hay contexto")
        return {
            "texto": "No se encontró información suficiente.",
            "resumen": "sin-datos"
        }




    for nota in top_noticias:
        nota.get('url')
        
        textos = []

        for agregar in noticias:
            if agregar.get('url') == nota.get('url'):
                textos.append(agregar.get('texto', ''))
                break
    
    contexto = " ".join(textos)
    print("CONTEXTO FINAL PARA EL LLM:\n", contexto)
    respuesta = generar_contenido(contexto,query=query)
    #logger.info(f"RAW LLM RESPONSE:\n{respuesta}")
    data = parsear_json_seguro(respuesta)

    return data