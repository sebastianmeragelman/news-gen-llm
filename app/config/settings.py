#---------------------------------------------#
#
# IMPORTO LAS VARIABLES DE ENTORNO PARA LA CONFIGURACIÓN DE LA APLICACIÓN
#
#---------------------------------------------#


import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")