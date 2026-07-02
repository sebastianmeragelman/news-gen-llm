# -------------------------------#
#
# DEFINO LAS FUNCIONES DE SERVICIO PARA GENERAR NOTICIAS
#
# -------------------------------#



from app.llm.groq_client import generar_contenido, filtrar_contenido, generar_contenido_html
from app.utils.logger import logger
import requests


def generar_noticia(query: str,max_links: int = 30,cant_imagenes: int = 1):
    """
    Funcion para generar una noticia a partir de una query, obteniendo links de noticias, filtrando el contenido y generando un resumen.
    Parámetros:
    - query: La query de búsqueda (string).
    - max_links: Número máximo de links a obtener (int, opcional, default=30).
    - cant_imagenes: Cantidad de imágenes a obtener (int, opcional, default=1).
    Retorna:
    - Un diccionario con el texto de la noticia, el resumen y una lista con los links a las imágenes.
    """

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
    top_noticias = filtrar_contenido(noticias,query)
    # Extraigo el cuerpo de la noticia porque viene en formato noticia:{texto:}
    top_noticias = top_noticias.get('noticias')

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
                
                
                textos.append(agregar.get('texto', ''))
                break
    
    # Genero el contexto concatenando los textos de las noticias filtradas
    contexto = " ".join(textos)
    
    # Obtengo la noticia generada a partir del contexto y la query, que incluye el resumen
    respuesta = generar_contenido(contexto,query=query)
   
    logger.info(respuesta)

    # Ejecutamos la llamada a la API para obtener imágenes relacionadas con la noticia generada
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
        return { "imagenes":["SIN IMAGENES"] }
    respuesta["imagenes"] = imagenes.get('imagenes')
    return respuesta



def generar_notica_html(query: str,max_links: int = 30,cant_imagenes: int = 1):
    """
    Funcion para generar una noticia en formato HTML a partir de una query, obteniendo links de noticias, filtrando el contenido y generando un resumen.
    Parámetros:
    - query: La query de búsqueda (string).
    - max_links: Número máximo de links a obtener (int, opcional, default=30).
    - cant_imagenes: Cantidad de imágenes a obtener (int, opcional, default=1).
    Retorna:
    - Un diccionario con el texto de la noticia, el resumen y una lista con los links a las imágenes, además del contenido formateado en HTML.  
    """
    noticia = generar_noticia(query,max_links,cant_imagenes)
    noticia_formateada = generar_contenido_html(noticia.get('texto'))
    noticia['noticia_formateada'] = noticia_formateada
    return noticia

