# -------------------------------#
#
# DEFINO LAS ESTRUCTURAS DE DATOS DEL JSON
#
# -------------------------------#


from pydantic import BaseModel, Field
from typing import List


class Noticia(BaseModel):
    titulo: str
    url: str
    orden: int


class ListaNoticias(BaseModel):
    noticias: List[Noticia]



class QueryInput(BaseModel):
    query: str

class NoticiaOutput(BaseModel):
    texto: str
    resumen: str