# -------------------------------#
#
# EJECUTO LLAMADA A GROQ PARA GENERAR CONTENIDO
#
# -------------------------------#



from groq import Groq
from app.config.settings import GROQ_API_KEY
from app.llm.prompt import generar_prompt_noticia



client = Groq(api_key=GROQ_API_KEY)

def generar_contenido(contexto: str):

    prompt = generar_prompt_noticia(contexto)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content