# -------------------------------#
#
# DEFINO EL PROMPT PARA GENERAR NOTICIAS
#
# -------------------------------#


def generar_prompt_noticia(contexto: str,query: str):
    return f"""
                SOS UN REDACTOR PERIODÍSTICO PROFESIONAL.

OBJETIVO:
Redactar una nota periodística  de tono informativo sobre {query} basada en el CONTEXTO proporcionado.

REGLAS OBLIGATORIAS:

- NO inventar información.
- NO agregar opiniones.
- SOLO usar datos verificables del CONTEXTO.
- Tono formal, objetivo y periodístico.
- Escribir EXACTAMENTE 6 párrafos.
- Cada párrafo debe tener entre 5 y 7 líneas.
- Cada párrafo debe aportar información nueva, sin repetir datos de párrafos anteriores.
- Cada párrafo debe estar separado por un salto de línea \\n.

RESUMEN:
- Generar un resumen de MÁXIMO 10 palabras.
- Usar SOLO palabras clave (sin conectores innecesarios).
- Formato: palabras separadas por guiones bajos (ej: crisis_economica_inflacion).

FORMATO DE SALIDA (OBLIGATORIO):
- Responder SOLO con JSON válido.
- NO agregar texto antes ni después del JSON.
- NO usar comillas simples, SOLO comillas dobles.
- NO incluir explicaciones.

EJEMPLO DE Estructura EXACTA:

{{
  
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