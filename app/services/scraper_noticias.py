from app.scrapers.news_scraper import  obtener_links
from app.models.schemas import Noticia, ListaNoticias
from app.utils.logger import logger
from app.scrapers.news_scraper import build_google_news_url, resolver_url, es_url_valida, extraer_texto, sanitizar
import requests
from playwright.sync_api import sync_playwright


def obtener_noticias(query: str, max_links: int = 30) -> ListaNoticias:

    rss_url = build_google_news_url(query)
    # MODIFICAR LA CANTIDAD DE LINKS PARA TENER MAYOR AMPLITUD DE CASOS
    raw_links = obtener_links(rss_url, max_links=max_links)


    ###################################
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
    ###############################


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
        

        for item in raw_links:

            try:
                logger.info(f"🔎 Procesando: {item['url']}")
                url_final = resolver_url(context, item["url"])
                if not url_final:
                    continue
                logger.info(f"➡ URL final: {url_final}")
                if "news.google.com" in url_final:
                    continue
                if not es_url_valida(url_final):
                    logger.warning("URL filtrada por blacklist")
                    continue
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
                if len(resultados) >= max_links:
                    break
            except Exception as e:
                logger.error(f" Error procesando item: {e}")
                continue
        browser.close()
    logger.info(f"Contextos obtenidos: {len(resultados)}")
    print("##################################")
    print(" ------ LOG RESULTADOS FINALES ------")
    print(resultados)
    print("##################################")
    
    return ListaNoticias(noticias=resultados)
    