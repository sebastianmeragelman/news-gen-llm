from app.scrapers.image_unsplash import obtener_imagenes_unsplash
from app.scrapers.image_pollinations import generate_image_pollinations


def obtener_imagenes(query: str, cantidad: int = 1):
    """
    Funcion para obtener imágenes relacionadas con una consulta dada.
    Parámetros:
    - query: Término de búsqueda (string).
    - cantidad: Número de imágenes a obtener (int, opcional, default=1).
    Retorna:
    - Un diccionario con la consulta y una lista de URLs de imágenes. {"query":str, "imagenes": [urls]}
    """    

    try:
       # Obtener imágenes desde la API de Unsplash
       urls = obtener_imagenes_unsplash(query,per_page=cantidad)
    except Exception as e:
        print(f"La API de UNSPLASH fallo {e}")

    if not urls:
        urls = []
    

        # Iteramos sobre el query para obtener imágenes desde la API de Pollinations
        for cant_imagenes in range(cantidad):
            query_limpia = query.replace("_", " ").strip()
            query_partes = query_limpia.split()


            if len(query_partes)-cant_imagenes <= 0:
                break
            else:
                
                query_unida = "_".join(query_partes[:len(query_partes)-cant_imagenes])
            
                # Construyo el listado de urls con las imágenes generadas por la API de Pollinations
                urls.append(generate_image_pollinations(query_unida,formato="realistic",width=500,height=500))


    return {
        "query": query,
        "imagenes": urls
    }
