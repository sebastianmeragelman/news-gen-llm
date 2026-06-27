import re
import requests


def generate_image_pollinations(resumen: str, formato: str, width: int = 512, height: int = 512):
    
    resumen_limpio = resumen.lower()

    # Reemplazamos acentos comunes si los hubiera
    acentos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    for origen, destino in acentos.items():
        resumen_limpio = resumen_limpio.replace(origen, destino)

    # Eliminamos cualquier carácter que NO sea una letra, número o espacio
    resumen_limpio = re.sub(r"[^a-z0-9\s]", "", resumen_limpio)
    
    
    url = f"https://image.pollinations.ai/p/{resumen_limpio}-{formato}?width={width}&height={height}&seed=42"

    response = requests.get(url)

    if response.status_code == 200:
        return url

