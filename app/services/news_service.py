# -------------------------------#
#
# DEFINO LAS FUNCIONES DE SERVICIO PARA GENERAR NOTICIAS
#
# -------------------------------#



from app.llm.groq_client import generar_contenido, filtrar_contenido
from app.utils.parser import parsear_json_seguro, limpiar_json_string
from app.utils.logger import logger
import requests
from app.services.scraper_noticias import obtener_noticias
import json



def generar_noticia(query: str,max_links: int = 30):

    logger.info(f"🚀 Nueva request: {query}")



    # Si corre en el puerto predeterminado de FastAPI, es el 8000
    url_scrape_noticias = "http://127.0.0.1:8000/scrape-noticias"

    # 2. Payload (JSON) que espera el endpoint
    payload = {"query": query, "max_links": max_links}

    try:
        #Petición POST mandando el JSON
        response = requests.post(url_scrape_noticias, json=payload)

        # Si el endpoint devuelve un error (400, 500, etc.), esto lanzará una excepción
        response.raise_for_status()

        # Obtener la lista de noticias desde la respuesta JSON
        
        noticias = response.json()

    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al obtener noticias: {e}")
        return {
            "texto": "No se pudo obtener información de noticias.",
            "resumen": "error"
        }

    

    logger.info(f"📄 Contexto generado: {len(noticias)} elementos")

    # Llamada al llm

    
    print("###############################")
    print("##########noticias antes de filtrar_contenido #####################")
    print(noticias)
    print("###############################")
    #noticias = json.loads(noticias)
    
    noticias = noticias.get('noticias')


    top_noticias = filtrar_contenido(noticias,query)
    top_noticias = top_noticias.get('noticias')
    
        
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
    #data = parsear_json_seguro(respuesta)

    #print("############ DATA:\n", data)
    print("##### LOG  parsear_json_seguro() PASA OK #####")
    #return data
    #return json.loads(respuesta)
    respuesta = generar_contenido(contexto, query=query)
    
    logger.info(respuesta)

    return respuesta