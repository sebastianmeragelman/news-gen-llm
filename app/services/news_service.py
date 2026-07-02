# -------------------------------#
#
# DEFINO LAS FUNCIONES DE SERVICIO PARA GENERAR NOTICIAS
#
# -------------------------------#



from app.llm.groq_client import generar_contenido, filtrar_contenido
from app.utils.logger import logger
import requests


def generar_noticia(query: str,max_links: int = 30,cant_imagenes: int = 1):

    logger.info(f"🚀 Nueva request: {query}")

    # Se llama a la API para obtener N cantidad de noticias sobre query
    # Si corre en el puerto predeterminado de FastAPI, es el 8000
    url_scrape_noticias = "http://127.0.0.1:8000/scrape-noticias"

    # 2. Payload (JSON) que espera el endpoint
    payload = {"query": query, "max_links": max_links}

    try:
        #Petición POST mandando el JSON - response tiene las noticias
        response = requests.post(url_scrape_noticias, json=payload)

        # Si el endpoint devuelve un error (400, 500, etc.), esto lanzará una excepción
        response.raise_for_status()

        # Obtener la lista de noticias (sin filtrar) desde la respuesta JSON
        noticias = response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al obtener noticias: {e}")
        return {
            "texto": "No se pudo obtener información de noticias.",
            "resumen": "error"
        }

    logger.info(f"📄 Contexto generado: {len(noticias.get('noticias', []))} elementos")

    # Extraigo el cuerpo de la noticia porque viene en formato noticia:{texto:}
    noticias = noticias.get('noticias')


    # Filtrar las noticias para quedarse con las más relevantes según la query
    
    
    print("#######################################")
    print("#############FILTRAR_NOTICIAS dentro de news_service##########################")
    print(" EJECUTO FILTRAR CONTENIDO")
    
    top_noticias = filtrar_contenido(noticias,query)
    top_noticias = top_noticias.get('noticias')

    print("#######################################")
    print("#############FILTRAR_NOTICIAS dentro de news_service##########################")
    print("  FILTRAR CONTENIDO FUNCIONO OK")


    # Para control del tamaño del contexto
    cantidad_palabras = 0
    for nota in top_noticias:
        cantidad_palabras += len(nota.get('texto', '').split())
    logger.info(f"📄 TAMAÑO DEL Contexto NOTICIAS generado: {cantidad_palabras} elementos")


        
    if not top_noticias:
        logger.warning("⚠️ No hay contexto")
        return {
            "texto": "No se encontró información suficiente.",
            "resumen": "sin-datos"
        }

    # Se genera el contexto concatenando los textos de las noticias filtradas
    textos = []
    
    # Itero sobre las noticias filtradas y busco el texto completo en la lista original
    for nota in top_noticias:
                
        # Busco la noticia en la lista original para obtener el texto completo
        for agregar in noticias:
            
            #Si la url de la noticia filtrada coincide con la url de la noticia original, agrego el texto completo
            if agregar.get('url') == nota.get('url'):
                
                print("#######################")
                print(f"########## TEXTO DE NOTICIA A SUMAR AL CONTEXTO {nota.get('url')} ##########")
                print(f"TAMAÑO EN PALABRAS: {len(agregar.get('texto', '').split())}")
                print(agregar.get('texto', ''))
                
                
                textos.append(agregar.get('texto', ''))
                break
    
    contexto = " ".join(textos)
    
    respuesta = generar_contenido(contexto,query=query)
   
    logger.info(respuesta)


    # Si corre en el puerto predeterminado de FastAPI, es el 8000
    url_imagenes = "http://127.0.0.1:8000/imagenes"

    # 2. Payload (JSON) que espera el endpoint
    payload = {"query": respuesta.get('resumen'), "cantidad": cant_imagenes}

    try:
        #Petición POST mandando el JSON
        response = requests.post(url_imagenes, json=payload)

        # Si el endpoint devuelve un error (400, 500, etc.), esto lanzará una excepción
        response.raise_for_status()

        # Obtener la lista de noticias desde la respuesta JSON
        
        imagenes = response.json()

    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al obtener imagenes: {e}")
        return {
            ["SIN IMAGENES"]
            
        }
    respuesta["imagenes"] = imagenes.get('imagenes')
    return respuesta





    return respuesta