from groq import Groq
from app.config.settings import GROQ_API_KEY
from app.llm.prompt import generar_prompt_noticia, filtrar_prompt_noticia
import instructor
from app.models.schemas import ListaNoticias,NoticiaGenerada

# Cliente base nativo
client = Groq(api_key=GROQ_API_KEY)

# Cliente extendido con Instructor (reutiliza el cliente base)
cliente_2 = instructor.from_groq(client)



def generar_contenido(contexto: str, query: str):
    print(" |||||||||||||||||||||||||||||||||||||||||||||")
    print(" CONTEXTO PARA EL LLM:\n", contexto)
    print(" |||||||||||||||||||||||||||||||||||||||||||||")

    prompt = generar_prompt_noticia(contexto, query=query)
    
    print("##### LOG  generar_prompt_noticia() PASA OK #####")

    response = cliente_2.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_model=NoticiaGenerada,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5 
    )
    # Devuelve un string (Texto plano)
    return response.model_dump()
    


def filtrar_contenido(noticias: list, query: str):
    prompt = filtrar_prompt_noticia(noticias, query=query)
    
    # CORRECCIÓN 1: Faltaba una coma (,) después de response_model=ListaNoticias
    response = cliente_2.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_model=ListaNoticias, 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1 # SUGERENCIA: Para filtrar/estructurar JSON usa temperaturas bajas (0.0 a 0.2)
    )

    # Devuelve un objeto de tipo ListaNoticias (Pydantic)
    return response.model_dump()

    