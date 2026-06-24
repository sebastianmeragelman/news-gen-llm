import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from app.utils.logger import logger
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

# ---------------------------------------------
# Construir URL RSS
# ---------------------------------------------
def build_google_news_url(query: str) -> str:
    
    print(f"https://news.google.com/rss/search?q="
        + quote(f"{query} when:7d")
        + "&hl=es-419&gl=AR&ceid=AR:es-419")

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
            pub_date = item.pubDate.text

            if not es_reciente(pub_date, dias=7):
                continue

            links.append(item.link.text)

            if len(links) >= max_links:
                break

        except Exception as e:
            logger.warning(f"Error procesando item RSS: {e}")
            continue

    logger.info(f"Links filtrados por fecha: {len(links)}")

    return links


def es_reciente(pub_date: str, dias: int = 7) -> bool:
    """
    Retorna True si la noticia tiene menos de X días de antigüedad
    """

    try:
        fecha_noticia = parsedate_to_datetime(pub_date)
        limite = datetime.now(fecha_noticia.tzinfo) - timedelta(days=dias)

        return fecha_noticia >= limite

    except Exception as e:
        logger.warning(f"Error parseando fecha pubDate: {e}")
        return False


# ---------------------------------------------
# Filtrar dominios
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

    logger.info(f"🧾 Párrafos encontrados: {len(paragraphs)}")

    texto = " ".join(p.get_text() for p in paragraphs)

    return texto


# ---------------------------------------------
# Sanitizar texto (mejorado)
# ---------------------------------------------
def sanitizar(texto: str) -> str:
    texto = re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,:;()\- ]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


# ---------------------------------------------
# Scraping principal
# ---------------------------------------------
def get_news_context(query: str, n: int = 3):

    rss_url = build_google_news_url(query)
    links = obtener_links(rss_url, max_links=40)

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "es-AR,es;q=0.9"
    }

    resultados = []

    if not links:
        logger.warning("⚠ No se encontraron links")
        return resultados

    #  UN SOLO BROWSER
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for link in links:

            try:
                logger.info(f"🔎 Procesando: {link}")

                page.goto(link, timeout=10000)
                page.wait_for_timeout(1500)  # clave para redirect

                url_final = page.url

                logger.info(f"➡ URL final: {url_final}")

                # evitar quedarse en Google News
                if not url_final or "news.google.com" in url_final:
                    logger.warning("❌ URL inválida (Google News)")
                    continue

                if not es_url_valida(url_final):
                    logger.warning("❌ URL filtrada por blacklist")
                    continue

                # scraping del artículo real
                response = requests.get(url_final, headers=headers, timeout=5)

                if response.status_code != 200:
                    logger.warning(f"❌ Status inválido: {response.status_code}")
                    continue

                texto = extraer_texto(response.text)

                if len(texto) < 300:
                    logger.warning("❌ Texto demasiado corto")
                    continue

                texto = sanitizar(texto)[:4000]

                resultados.append(f"\n{texto}")

                if len(resultados) >= n:
                    break

            except Exception as e:
                logger.error(f"🔥 Error procesando {link}: {e}")
                continue

        browser.close()

    logger.info(f" Contextos obtenidos: {len(resultados)}")

    return resultados