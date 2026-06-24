# ---------------------------------------------#
#
# ESTE ARCHIVO SE ENCAERGA DE SCRAPEAR NOTICIAS DE INTERNET UTILIZANDO EL MOTOR DE BÚSQUEDA DDG (DuckDuckGo)
#
#
# ---------------------------------------------#

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from urllib.parse import urlparse


# 🔒 Filtro de dominios no deseados
def es_url_valida(url: str) -> bool:
    blacklist = [
        "instagram.com",
        "facebook.com",
        "twitter.com",
        "x.com",
        "youtube.com",
        "youtu.be",
        "tiktok.com",
        "linkedin.com"
    ]

    dominio = urlparse(url).netloc.lower()
    return not any(b in dominio for b in blacklist)


# 🧹 Limpieza de texto HTML
def extraer_texto_limpio(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # eliminar scripts y estilos
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # extraer párrafos (mejor que get_text plano)
    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text() for p in paragraphs)

    # limpiar espacios
    text = " ".join(text.split())

    return text


# 🔍 Función principal
def buscador(query: str, n_resultados: int = 3):

    headers = {"User-Agent": "Mozilla/5.0"}
    resultados_finales = []

    # Traemos más resultados porque vamos a filtrar
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=n_resultados * 3))

    for r in results:
        url = r.get("href", "")

        # 🚫 Filtrar redes sociales
        if not es_url_valida(url):
            continue

        try:
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code != 200:
                continue

            text = extraer_texto_limpio(response.text)

            # 🚫 descartar contenido pobre
            if len(text) < 300:
                continue

            # ✂ limitar tamaño (para LLM)
            text = text[:3000]

            resultados_finales.append({
                "url": url,
                "title": r.get("title", ""),
                "text": text
            })

            # 🎯 cortar cuando llegamos a N buenos
            if len(resultados_finales) >= n_resultados:
                break

        except Exception:
            continue

    return resultados_finales