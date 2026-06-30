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
    return (
        "https://news.google.com/rss/search?q="
        + quote(f"{query} when:7d")
        + "&hl=es-419&gl=AR&ceid=AR:es-419"
    )


# ---------------------------------------------
# Obtener links desde RSS
# ---------------------------------------------
def obtener_links(rss_url: str, max_links: int = 30):
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

    page = context.new_page()

    try:
        page.goto(
            url,
            timeout=10000,
            wait_until="domcontentloaded"
        )

        page.wait_for_timeout(2000)

        return page.url

    finally:
        page.close()

# ---------------------------------------------
# Validar dominio
# ---------------------------------------------
def es_url_valida(url: str) -> bool:
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
    texto = re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,:;()\- ]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto
