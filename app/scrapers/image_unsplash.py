from app.config.settings import UNSPLASH_API_KEY
import requests



def obtener_imagenes_unsplash(query: str, per_page: int = 1, page: int = 1, orientation: str = "landscape"):
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

    print("IMPRIMO LOG RESPONSE:")
    print(response)



    url_imagenes = []
    if response.status_code == 200:
        datos = response.json()
        
        
        # Iterar sobre los resultados para obtener las URLs de las imágenes
        for foto in datos['results']:
            print(f"Imagen encontrada: {foto['urls']['regular']}")  # URL de la imagen en alta resolución
            url_imagenes.append(foto['urls']['regular']) # URL de la imagen en alta resolución
    else:
        print(f"Error: {response.status_code}")
        raise RuntimeError(f"Unsplash API falló con estado: {response.status_code}")
    
    
    
    return url_imagenes