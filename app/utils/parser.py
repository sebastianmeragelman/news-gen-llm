# ---------------------------------------------#
#
# ESTE ARCHIVO SE ENCARGA DE PARSEAR RESPUESTAS DE LOS LLM Y CONVERTIRLAS EN JSON VÁLIDO
#
# ---------------------------------------------#


import json
import re


def limpiar_json_string(texto: str) -> str:
    """
    Limpia basura típica que devuelven los LLM:
    - ```json ... ```
    - texto antes o después del JSON
    """

    # eliminar bloques tipo ```json ... ```
    texto = re.sub(r"```json", "", texto)
    texto = re.sub(r"```", "", texto)

    # buscar primer { y último }
    inicio = texto.find("{")
    fin = texto.rfind("}")

    if inicio != -1 and fin != -1:
        texto = texto[inicio:fin+1]

    return texto.strip()


def parsear_json_seguro(texto: str) -> dict:
    """
    Intenta convertir la respuesta del LLM en JSON válido.
    Tiene fallback para evitar que rompa la API.
    """

    try:
        limpio = limpiar_json_string(texto)

        data = json.loads(limpio)

        # Validación mínima
        if "texto" not in data or "resumen" not in data:
            raise ValueError("JSON incompleto")

        return data

    except Exception as e:
        #  fallback seguro
        return {
            "texto": "No se pudo generar la noticia correctamente.",
            "resumen": "error-generacion"
        }