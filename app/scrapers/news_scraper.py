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
            wait_until="networkidle"
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

    logger.info(f"🧾 Párrafos encontrados: {len(paragraphs)}")

    return " ".join(p.get_text() for p in paragraphs)


# ---------------------------------------------
# Sanitizar texto
# ---------------------------------------------
def sanitizar(texto: str) -> str:
    texto = re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,:;()\- ]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


# ---------------------------------------------
# SCRAPING PRINCIPAL (REFACTO MÍNIMO)
# ---------------------------------------------
def get_news_context(query: str, n: int = 3):

    rss_url = build_google_news_url(query)
    # MODIFICAR LA CANTIDAD DE LINKS PARA TENER MAYOR AMPLITUD DE CASOS
    raw_links = obtener_links(rss_url, max_links=30)

    #headers = {
    #    "User-Agent": "Mozilla/5.0",
    #    "Accept-Language": "es-AR,es;q=0.9"
    #}



    headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",

    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",

    "Accept-Language":
    "es-AR,es;q=0.9",

    "Accept-Encoding":
    "gzip, deflate, br",

    "Connection":
    "keep-alive",

    "Upgrade-Insecure-Requests":
    "1"
    }

    resultados = []

    if not raw_links:
        logger.warning("⚠ No se encontraron links")
        return resultados

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=headers["User-Agent"],
            locale="es-AR"
        )
        #page = context.new_page()

        for item in raw_links:

            try:
                logger.info(f"🔎 Procesando: {item['url']}")

                #url_final = resolver_url(page, item["url"])
                url_final = resolver_url(context, item["url"])
                if not url_final:
                    continue

                logger.info(f"➡ URL final: {url_final}")
                
                if "news.google.com" in url_final:
                    continue

                if not es_url_valida(url_final):
                    logger.warning("❌ URL filtrada por blacklist")
                    continue

                # intento de acceso real
                try:
                    response = requests.get(
                        url_final,
                        headers=headers,
                        timeout=8
                    )

                    if response.status_code == 200:
                        html = response.text

                    elif response.status_code == 403:
                        logger.info("⚠ 403 detectado, intentando con Playwright...")

                        page = context.new_page()

                        try:
                            page.goto(
                                url_final,
                                wait_until="networkidle",
                                timeout=30000
                            )

                            html = page.content()
                            
                            print("##################################")
                            print(" ------ LOG HTML PLAYWRIGHT ------")
                            print(html[:340])
                            print("##################################")


                        finally:
                            page.close()

                    else:
                        logger.warning(f"Status inválido: {response.status_code}")
                        continue

                except Exception as e:
                    logger.warning(f"Error HTTP: {e}")
                    continue

                texto = extraer_texto(html)
                if len(texto) < 300:
                    continue

                texto = sanitizar(texto)[:4000]

                resultados.append({
                    "url": url_final,
                    "titulo": item.get("titulo", ""),
                    "texto": texto
                })

                if len(resultados) >= n:
                    break

            except Exception as e:
                logger.error(f"🔥 Error procesando item: {e}")
                continue

        browser.close()

    logger.info(f"✅ Contextos obtenidos: {len(resultados)}")

    return resultados