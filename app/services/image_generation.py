from app.scrapers.image_unsplash import obtener_imagenes_unsplash
from app.models.schemas import ImagenesOutput
from app.scrapers.image_pollinations import generate_image_pollinations




def obtener_imagenes(query: str, cantidad: int = 1):
    
    print("------------------------------------------")
    print("----- INGRESO EN OBTENER IMAGENES -----------")
    print("------------------------------------------")

    try:
       urls = obtener_imagenes_unsplash(query,per_page=cantidad)
    except Exception as e:
        print(f"La API de UNSPLASH fallo {e}")

    if not urls:
        urls = []
    
        for cant_imagenes in range(cantidad):
            query_limpia = query.replace("_", " ").strip()
            query_partes = query_limpia.split()

            print("######################")
            print("########QUERY_PARTES##############")
            print(query_partes)
            print("######################")

            if len(query_partes)-cant_imagenes <= 0:
                break
            else:
                
                query_unida = "_".join(query_partes[:len(query_partes)-cant_imagenes])
                print("######################")
                print("########QUERY_UNIDA##############")
                print(query_unida)
                print("######################")

                urls.append(generate_image_pollinations(query_unida,formato="realistic",width=500,height=500))


    return {
        "query": query,
        "imagenes": urls
    }
