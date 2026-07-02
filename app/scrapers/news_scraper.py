import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from app.utils.logger import logger
from email.utils import parsedate_to_datetime


# ---------------------------------------------
# Construir URL RSS
# ---------------------------------------------
def build_google_news_url(query: str) -> str:
    """
    Construye la URL del RSS de Google News para una consulta dada.
    Parámetros:
    - query: Término de búsqueda (string).
    Retorna:
    - La URL del RSS de Google News (string).
    """

    return (
        "https://news.google.com/rss/search?q="
        + quote(f"{query} when:7d")
        + "&hl=es-419&gl=AR&ceid=AR:es-419"
    )


# ---------------------------------------------
# Obtener links desde RSS
# ---------------------------------------------
def obtener_links(rss_url: str, max_links: int = 30):
    """
    Funcion para obtener links de noticias desde un feed RSS.
    Parámetros:
    - rss_url: URL del feed RSS (string).       
    - max_links: Número máximo de links a obtener (int, opcional, default=30).
    Retorna:
    - Una lista de diccionarios con 'url' y 'titulo' de las noticias
    """
    
    # Realizar la petición al feed RSS y parsear el contenido XML
    response = requests.get(rss_url, timeout=5)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")

    links = []
    for item in items:
        try:
            links.append({
                "url": item.link.text,
                "titulo": item.title.text if item.title else ""
            })
            # Si hemos alcanzado el número máximo de links, salimos del bucle
            if len(links) >= max_links:
                break
        except Exception as e:
            logger.warning(f"Error RSS item: {e}")
            continue

    logger.info(f"Links obtenidos: {len(links)}")
    return links


# ---------------------------------------------
# Resolver URL real (redir Google News → sitio final)
# ---------------------------------------------
def resolver_url(context, url):
    """
    Funcion para resolver la URL real de una noticia a partir de la URL de Google News.
    Parámetros:
    - context: Contexto de Playwright (Playwright context).
    - url: URL de Google News (string).
    Retorna:
    - La URL real de la noticia (string).
    """
    page = context.new_page()

    try:
        page.goto(
            url,
            # Parametros para esperar a que la página cargue completamente
            timeout=10000,
            wait_until="domcontentloaded"
        )
        page.wait_for_timeout(2000)
        # Devuelvo la pagina real
        return page.url

    finally:
        page.close()

# ---------------------------------------------
# Validar dominio
# ---------------------------------------------
def es_url_valida(url: str) -> bool:
    """
    Funcion para filtrar URLs de noticias que no sean de redes sociales.
    """
    
    blacklist = [
        "instagram.com", "facebook.com", "twitter.com",
        "x.com", "youtube.com", "youtu.be",
        "tiktok.com", "linkedin.com"
    ]

    dominio = urlparse(url).netloc.lower()
    return not any(b in dominio for b in blacklist)


# ---------------------------------------------
# Extraer texto HTML
# ---------------------------------------------
def extraer_texto(html: str) -> str:
    """
    Funcion para extraer el texto de un HTML, eliminando scripts, estilos y etiquetas innecesarias.
    """
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    paragraphs = soup.find_all("p")

    logger.info(f" Párrafos encontrados: {len(paragraphs)}")

    return " ".join(p.get_text() for p in paragraphs)


# ---------------------------------------------
# Sanitizar texto
# ---------------------------------------------
def sanitizar(texto: str) -> str:
    """
    Funcion para sanitizar el texto, eliminando caracteres especiales y normalizando espacios.
    """
    texto = re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,:;()\- ]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto
