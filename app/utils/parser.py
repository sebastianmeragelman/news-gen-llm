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





def sanitizar_json_llm(texto: str) -> str:
    """
    Intenta corregir JSON roto típico de LLM:
    - comillas internas sin escape
    - backslashes mal formados
    - saltos de línea dentro de strings
    """

    # 1. eliminar ```json ``` si existen
    texto = re.sub(r"```json", "", texto)
    texto = re.sub(r"```", "", texto)

    # 2. eliminar saltos de línea dentro de strings (causa MUY común de crash)
    texto = re.sub(r'(?<!\\)\n', " ", texto)

    # 3. normalizar comillas “inteligentes”
    texto = texto.replace("“", '"').replace("”", '"')

    # 4. escapar comillas dentro de strings de forma básica
    # (esto no es perfecto, pero salva muchos casos)
    texto = re.sub(r'(?<=[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ])"(?=[a-zA-Z])', '\\"', texto)

    # 5. limpiar dobles espacios
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto




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



def noticias_json_seguro(texto: str) -> dict:
    """
    Intenta convertir la respuesta del LLM en JSON válido.
    Tiene fallback para evitar que rompa la API.
    """

    try:
        limpio = limpiar_json_string(texto)

        data = json.loads(limpio)

        # Validación mínima
        if "url" not in data or "titulo" not in data:
            raise ValueError("JSON incompleto")

        return data

    except Exception as e:
        return {
            "titulo": "Error de generación",
            "texto": "No se pudo generar la noticia correctamente.",
            "resumen": "error-generacion"
        }