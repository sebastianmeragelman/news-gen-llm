# -------------------------------#
#
# DEFINO LAS ESTRUCTURAS DE DATOS DEL JSON
#
# -------------------------------#


from pydantic import BaseModel, Field
from typing import List



class ImagenesOutput(BaseModel):
    query: str
    imagenes: List[str]

class Noticia(BaseModel):
    titulo: str
    url: str
    orden: int


class ListaNoticias(BaseModel):
    noticias: List[Noticia]



class QueryInput(BaseModel):
    query: str

class NoticiaOutput(BaseModel):
    titulo: str
    texto: str
    resumen: str


class NoticiaGenerada(BaseModel):
    titulo: str
    texto: str
    resumen: str