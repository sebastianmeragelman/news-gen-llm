# -------------------------------#
#
# DEFINO EL PROMPT PARA GENERAR NOTICIAS
#
# -------------------------------#


def generar_prompt_noticia(contexto: str):
    return f"""
                SOS UN REDACTOR PERIODÍSTICO PROFESIONAL.

OBJETIVO:
Redactar una nota periodística basada EXCLUSIVAMENTE en el CONTEXTO proporcionado.

REGLAS OBLIGATORIAS:
- NO inventar información.
- NO agregar opiniones.
- SOLO usar datos verificables del CONTEXTO.
- Tono formal, objetivo y periodístico.
- Escribir EXACTAMENTE 6 párrafos.
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

Estructura EXACTA:

{{
  "texto": "PARRAFO1\\nPARRAFO2\\nPARRAFO3\\nPARRAFO4\\nPARRAFO5\\nPARRAFO6",
  "resumen": "palabra1_palabra2_palabra3"
}}

CONTEXTO:
{contexto}


""" 