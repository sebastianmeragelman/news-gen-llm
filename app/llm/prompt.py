# -------------------------------#
#
# DEFINO EL PROMPT PARA GENERAR NOTICIAS
#
# -------------------------------#


def filtrar_prompt_noticia(noticias: list,query: str):
    """
    funcion para generar un prompt que filtra noticias a partir de una lista de noticias y una query dada.
    """

    lista_noticias = []
    for noticia in noticias:
        lista_noticias.append({
            "titulo": noticia.get("titulo", ""),
            "url": noticia.get("url", ""),
            "texto": noticia.get("texto", "")[:4000]
        })

    return f"""
                SOS UN PERIODISTA PROFESIONAL EN LA PROVINCIA DE CÓRDOBA, ARGENTINA.

OBJETIVO:
Ordenar las noticias por relevancia en relación a la busqueda: {query}.

REGLAS OBLIGATORIAS:
- Si una noticia ocurre en una provincia distinta de Córdoba,
su relevancia debe ser MENOR que cualquier noticia que ocurra
en Córdoba, incluso si trata exactamente el mismo tema.
- PRIORIZAR NOTICIAS QUE HABLEN DE CÓRDOBA, ARGENTINA.
- NO inventar información.
- Basar la relevancia de las noticias en funcion de los campos titulo y url
- NO agregar opiniones ni texto adicional.
- ORDENAR las noticias por relevancia DE MAYOR A MENOR.
- No repetir noticias.

CRITERIOS DE RELEVANCIA (EN ORDEN DE IMPORTANCIA)

1. Noticias que ocurren en la provincia de Córdoba o ciudad de Córdoba.
2. Noticias que mencionan ciudades cordobesas, por ejemplo:
   Córdoba Capital, Río Cuarto, Villa María,
   San Francisco, Alta Gracia, Carlos Paz,
   Cruz del Eje, Bell Ville, etc.
3. Noticias publicadas por medios cordobeses.
4. Noticias de otras provincias tienen menor prioridad,
   incluso si hablan del mismo tema.
5. Si una noticia corresponde a otra provincia
   (Santa Fe, Buenos Aires, Mendoza, Chaco,
   Río Negro, Neuquén, etc.) debe quedar al final.


FORMATO DE SALIDA (OBLIGATORIO):
- ARMAR UNA LISTA DE OBJETOS JSON CON 4 OBJETOS QUE DETERMINASTE QUE TIENEN MAYOR RELEVANCIA
- Responder SOLO con una LISTA de JSON válido.
- NO agregar texto antes ni después del JSON.
- NO incluir explicaciones.
- NO INCLUIR UNA NOTA ACLARATORIA
- UTILIZAR COMILLAS DOBLES (") Y NO SIMPLES (') PARA LOS CAMPOS DEL JSON


EJEMPLO DE Estructura EXACTA:

ENTRADA:
{{
"titulo": "Titulo de la noticia1",
"url": "https://www.ejemplo.com/noticia1",
"texto": "Texto de la noticia1"
}},
{{
"titulo": "Titulo de la noticia2",
"url": "https://www.ejemplo.com/noticia2",
"texto": "Texto de la noticia2"
}},
{{
"titulo": "Titulo de la noticia3",
"url": "https://www.ejemplo.com/noticia3",
"texto": "Texto de la noticia3"
}},
{{
"titulo": "Titulo de la noticia4",
"url": "https://www.ejemplo.com/noticia4",
"texto": "Texto de la noticia4"
}}

NOTICIAS DISPONIBLES EN EL CONTEXTO:
{lista_noticias}



"""     

def generar_prompt_formato_html(contexto: str):
    """
    Funcion para crear prompt que genera una nota periodística en formato HTML para WordPress a partir de un contexto dado.
    """
    
    return f"""  
SOS UN REDACTOR Y EDITOR PERIODÍSTICO PROFESIONAL.

OBJETIVO:
Redactar una nota periodística completa, formal y atractiva utilizando única y exclusivamente la información del CONTEXTO proporcionado. El texto generado se publicará directamente en un sitio web de WordPress.

REGLAS OBLIGATORIAS:
- SOLO usa datos verificables del CONTEXTO. No agregues opiniones ni inventes información.
- Omitir firmas de autor, fechas del cable original o textos de copyright.
- Tono estrictamente formal, objetivo y periodístico.

INSTRUCCIONES DE ESTRUCTURA Y FORMATO PARA WORDPRESS:

1. TITULO: Debe ser plano (sin etiquetas HTML), claro e informativo, de entre 5 y 12 palabras. (WordPress utiliza este campo para el <h1> automáticamente).

2. TEXTO: Debe estar estructurado exclusivamente con etiquetas HTML para WordPress. 
   - No incluyas un <h1> dentro del texto (el título ya cumple esa función).
   - Divide la nota en secciones lógicas utilizando subtítulos con la etiqueta <h2> ...<h2>.
   - Cada párrafo debe estar encerrado estrictamente entre etiquetas <p>...</p>.
   - Usa etiquetas <strong>...</strong> con moderación para destacar datos clave, cifras o nombres importantes.
   - IMPORTANTE: El contenido dentro de este campo debe sumar entre 250 y 550 palabras. No repitas frases para rellenar.

3. RESUMEN: Genera una síntesis de entre 2 y 4 palabras clave separadas por guiones bajos.

CONTEXTO:
{contexto}
    """

def generar_prompt_noticia(contexto: str,query: str):
    """
    Funcion para crear prompt que genera una nota periodística a partir de un contexto y una query dada.
    """
    
    return f"""
                SOS UN REDACTOR PERIODÍSTICO PROFESIONAL.

OBJETIVO:
Redactar una nota periodística sobre {query} reutilizando información del CONTEXTO proporcionado.

REGLAS OBLIGATORIAS:

- NO agregar opiniones.
- OMITIR LAS SECCIONES DE TEXTO QUE DIGAN COPYWRIGHT 
- SOLO usar datos verificables del CONTEXTO.
- Tono formal, objetivo y periodístico.
- El título debera tener un MINIMO de 5 palabras y un MÁXIMO 10 palabras.
- El total de la nota debe tener mas de 300 palabras y menos de 600 palabras.

TITULO: 
- Generar un título de MÁXIMO 10 palabras.
- Usar un lenguaje claro y conciso.

TEXTO:
- El total de la nota debe tener mas de 300 palabras y menos de 600 palabras.
- Ampliar la información con datos verificables del CONTEXTO.
- Se debe continuar la redacción de la nota hasta alcanzar el mínimo de 300 palabras o el maximo de 600 palabras.

RESUMEN:
- Generar un resumen de MINIMO 2 palabras y MÁXIMO 4 palabras.
- Usar SOLO palabras clave (sin conectores innecesarios).
- Formato: palabras separadas por guiones bajos (ej: crisis_economica_inflacion).


FORMATO DE SALIDA (OBLIGATORIO):
- Responder SOLO con JSON válido.
- NO agregar texto antes ni después del JSON.
- NO usar comillas simples, SOLO comillas dobles.
- NO incluir explicaciones.

EJEMPLO DE Estructura EXACTA:

{{
  "titulo": "Título de la noticia",
  "texto":  "texto de la nota", 
  "resumen": "palabra1_palabra2_palabra3"
}}

CONTEXTO:
{contexto}


""" 