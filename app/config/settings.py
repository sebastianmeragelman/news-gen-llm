#---------------------------------------------#
#
# IMPORTO LAS VARIABLES DE ENTORNO PARA LA CONFIGURACIÓN DE LA APLICACIÓN
#
#---------------------------------------------#


import os
from dotenv import load_dotenv

load_dotenv()

# API KEYS NECESARIAS PARA ACCEDER A LOS SERVICIOS DE GENERACIÓN DE CONTENIDO Y OBTENER IMÁGENES
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")