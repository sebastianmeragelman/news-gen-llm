import re
import requests


def generate_image_pollinations(resumen: str, formato: str, width: int = 512, height: int = 512):
    """
    Funcion para generar una imagen a partir de un resumen dado, utilizando la API de Pollinations.
    """
    resumen_limpio = resumen.lower()

    # Sanitizamos y reemplazamos acentos comunes si los hubiera
    acentos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    for origen, destino in acentos.items():
        resumen_limpio = resumen_limpio.replace(origen, destino)
    # Eliminamos cualquier carácter que NO sea una letra, número o espacio
    resumen_limpio = re.sub(r"[^a-z0-9\s]", "", resumen_limpio)
    
    # Armamos la URL para la API de Pollinations   
    url = f"https://image.pollinations.ai/p/{resumen_limpio}-{formato}?width={width}&height={height}&seed=42"
    # Obtenemos la imagen desde la URL generada por la API de Pollinations
    response = requests.get(url)

    if response.status_code == 200:
        return url

