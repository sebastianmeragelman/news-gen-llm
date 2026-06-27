from app.scrapers.image_unsplash import obtener_imagenes_unsplash
from app.models.schemas import ImagenesOutput
from app.scrapers.image_pollinations import generate_image_pollinations




def obtener_imagenes(query: str, cantidad: int = 1):
    
    try:
       urls = obtener_imagenes_unsplash(query,per_page=cantidad)
    except:

        urls = []
        for cant_imagenes in range(cantidad):
            query_partes = query.split()

            if len(query_partes)-cant_imagenes <= 0:
                break
            else:
                
                query_unida = "_".join(query_partes[:len(query_partes)-cant_imagenes])
                urls.append(generate_image_pollinations(query_unida,formato="realistic",width=500,height=500))


    return {
        "query": query,
        "imagenes": urls
    }
