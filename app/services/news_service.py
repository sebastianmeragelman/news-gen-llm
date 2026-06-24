# -------------------------------#
#
# DEFINO LAS FUNCIONES DE SERVICIO PARA GENERAR NOTICIAS
#
# -------------------------------#


from app.scrapers.ddg_scraper import buscador
from app.llm.groq_client import generar_contenido
from app.utils.parser import parsear_json_seguro

def generar_noticia(query: str):

    resultados = buscador(query, 3)

    contexto = "\n\n".join([r["text"] for r in resultados])

    respuesta = generar_contenido(contexto)

    data = parsear_json_seguro(respuesta)

    return data