# -------------------------------#
#
# EJECUTO LLAMADA A GROQ PARA GENERAR CONTENIDO
#
# -------------------------------#



from groq import Groq
from app.config.settings import GROQ_API_KEY
from app.llm.prompt import generar_prompt_noticia



client = Groq(api_key=GROQ_API_KEY)

def generar_contenido(contexto: str,query: str):

    print(" |||||||||||||||||||||||||||||||||||||||||||||")
    print(" CONTEXTO PARA EL LLM:\n", contexto)
    print(" |||||||||||||||||||||||||||||||||||||||||||||")

    prompt = generar_prompt_noticia(contexto,query=query)
    print("\n\nPROMPT GENERADO:\n", prompt)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5 
    )

    return response.choices[0].message.content