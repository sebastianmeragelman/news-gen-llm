from groq import Groq
from app.config.settings import GROQ_API_KEY
from app.llm.prompt import generar_prompt_noticia, filtrar_prompt_noticia,generar_prompt_formato_html
import instructor
from app.models.schemas import NoticiaGenerada,ListaNoticiasOrdenadas

# Cliente base nativo
client = Groq(api_key=GROQ_API_KEY)

# Cliente extendido con Instructor (reutiliza el cliente base)
cliente_2 = instructor.from_groq(client)



def generar_contenido_html(contenido):
    """
    Función para generar contenido para publicar en Wordpress en formato HTML a partir de un texto dado.
    """
    
    # Obtenemos el prompt para generar contenido en formato HTML / Ejecutamos llamada a GROQ
    prompt = generar_prompt_formato_html(contenido )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
        
    )
    # Devuelve un string (Texto plano)
    return response.choices[0].message.content


def generar_contenido(contexto: str, query: str):
    """
    Función para generar contenido a partir de un contexto (noticias escrapeadas) y una query dada.
    """
    
    # Obtenemos el prompt para generar contenido / Ejecutamos llamada a GROQ
    prompt = generar_prompt_noticia(contexto, query=query)
   

    response = cliente_2.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_model=NoticiaGenerada,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        frequency_penalty=0.5 
    )
    # Devuelve un string (Texto plano)
    return response.model_dump()
    

def filtrar_contenido(noticias: list, query: str):
    """
    Funcion para filtrar contenido a partir de una lista de noticias y una query dada.
    """
    
    # Obtenemos el prompt para filtrar contenido / Ejecutamos llamada a GROQ
    prompt = filtrar_prompt_noticia(noticias, query=query)
    response = cliente_2.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_model=ListaNoticiasOrdenadas, 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    # Devuelve un objeto de tipo ListaNoticias (Pydantic)
    return response.model_dump()

    