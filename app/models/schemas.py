# -------------------------------#
#
# DEFINO LAS ESTRUCTURAS DE DATOS DEL JSON
#
# -------------------------------#


from pydantic import BaseModel

class QueryInput(BaseModel):
    query: str

class NoticiaOutput(BaseModel):
    texto: str
    resumen: str