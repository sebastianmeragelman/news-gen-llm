# -------------------------------#
#
# DEFINO EL PROMPT PARA GENERAR NOTICIAS
#
# -------------------------------#


def filtrar_prompt_noticia(noticias: list,query: str):
    
    lista_noticias = []
    for noticia in noticias:
        lista_noticias.append({
            "titulo": noticia.get("titulo", ""),
            "url": noticia.get("url", ""),
            "texto": noticia.get("texto[:1000]", "")
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

SALIDA ESPERADA:
[{{
"titulo": "Titulo de la noticia1",
"url": "https://www.ejemplo.com/noticia1",
"orden": 1
}},
{{
"titulo": "Titulo de la noticia 4",
"url": "https://www.ejemplo.com/noticia4",
"orden": 2
}},
{{
"titulo": "Titulo de la noticia 2",
"url": "https://www.ejemplo.com/noticia2",
"orden": 3
}}
,
{{
"titulo": "Titulo de la noticia 3",
"url": "https://www.ejemplo.com/noticia3",
"orden": 4
}}
]


NO SE ACEPTARA UNA SALIDA QUE NO RESPONDA AL FORMATO DE LISTA  DE 4 OBJETOS JSON COMO: [{{}},{{}},{{}},{{}}] , NI QUE INCLUYA TEXTO ADICIONAL.

NOTICIAS:
{lista_noticias}


"""     


def generar_prompt_noticia(contexto: str,query: str):
    return f"""
                SOS UN REDACTOR PERIODÍSTICO PROFESIONAL.

OBJETIVO:
Redactar una nota periodística  de tono informativo sobre {query} basada en el CONTEXTO proporcionado.

REGLAS OBLIGATORIAS:

- NO agregar opiniones.
- OMITIR LAS SECCIONES DE TEXTO QUE DIGAN COPYWRIGHT 
- SOLO usar datos verificables del CONTEXTO.
- Tono formal, objetivo y periodístico.
- Cada párrafo debe estar separado por un salto de línea \\n.

NOTA:
- Ampliar la información con datos verificables del CONTEXTO.
- Ampliar la información con datos verificables en Wikipedia
- CADA PARRAFO DEBE TENER ENTRE 4 y 6 lineas.
- Escribir entre 5 y 6 párrafos.
- El total de la nota debe tener entre 300 y 600 palabras.
- Cada párrafo debe aportar información nueva, sin repetir datos de párrafos anteriores.

RESUMEN:
- Generar un resumen de MINIMO 4 palabras y MÁXIMO 6 palabras.
- Usar SOLO palabras clave (sin conectores innecesarios).
- Formato: palabras separadas por guiones bajos (ej: crisis_economica_inflacion).

TITULO: 
- Generar un título de MÁXIMO 10 palabras.
- Usar un lenguaje claro y conciso.

FORMATO DE SALIDA (OBLIGATORIO):
- Responder SOLO con JSON válido.
- NO agregar texto antes ni después del JSON.
- NO usar comillas simples, SOLO comillas dobles.
- NO incluir explicaciones.

EJEMPLO DE Estructura EXACTA:

{{
  "titulo": "Título de la noticia",
  "texto": 
  "<P1> ... </P1>
  <P2> ... </P2>
  <P3> ... </P3>
  <P4> ... </P4>
  <P5> ... </P5>
  <P6> ... </P6>", 
  "resumen": "palabra1_palabra2_palabra3"
}}

CONTEXTO:
{contexto}


""" 