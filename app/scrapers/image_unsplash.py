from app.config.settings import UNSPLASH_API_KEY
import requests



def obtener_imagenes_unsplash(query: str, per_page: int = 1, page: int = 1, orientation: str = "landscape"):
    """
    Función para obtener imágenes de Unsplash según una query dada.
    Parámetros:
    - query: Término de búsqueda (string).
    - per_page: Cantidad de imágenes por página (int, máximo 30).
    - page: Número de página de resultados (int).
    - orientation: Orientación de la imagen (string, opcional: "landscape", "portrait", "squarish").
    Retorna:
    - Una lista de URLs de imágenes (list).    
    """

    # Definimos la URL base de la API de Unsplash y los headers necesarios para la autenticación
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization":"Client-ID " + UNSPLASH_API_KEY
            }
    # Formateo de los parámetros de búsqueda
    params = {
        "query": query, # Tu término de búsqueda (puede llevar espacios)
        "per_page": per_page,                     # Cantidad de imágenes por página (Max 30)
        "page": page,                          # Número de página de resultados
        "orientation": orientation          # Opcional: filtro (landscape, portrait, squarish)
    }

    # Realizar la petición
    
    response = requests.get(url, headers=headers, params=params)
    url_imagenes = []
    if response.status_code == 200:
        datos = response.json()
        
        # Iterar sobre los resultados para obtener las URLs de las imágenes
        for foto in datos['results']:        
            # URL de la imagen en alta resolución
            url_imagenes.append(foto['urls']['regular']) 
    else:
        print(f"Error: {response.status_code}")
        raise RuntimeError(f"Unsplash API falló con estado: {response.status_code}")
    
    
    
    return url_imagenes