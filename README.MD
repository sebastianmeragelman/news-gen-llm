# NEWS-GEN-LLM

**Estado del proyecto:** En desarrollo activo

Versión actual: v0.1.0

Arquitectura: API REST modular


app/
│
├── api/
│   Endpoints REST expuestos por FastAPI.
│
├── config/
│   Configuración general del sistema y variables de entorno.
│
├── llm/
│   Clientes de acceso a los modelos de lenguaje y definición de prompts.
│
├── models/
│   Modelos Pydantic utilizados para validar requests y responses.
│
├── scrapers/
│   Obtención de información desde fuentes externas
│   (Google News, Unsplash y Pollinations).
│
├── services/
│   Lógica de negocio que orquesta scraping, generación
│   de contenido e imágenes.
│
├── utils/
│   Funciones auxiliares de logging, parsing y utilidades comunes.
│
└── main.py
    Punto de entrada de la aplicación.


API REST para la generación automática de contenido periodístico utilizando técnicas de Web Scraping y Large Language Models (LLM).

El sistema obtiene información desde múltiples medios digitales, procesa y filtra las noticias más relevantes mediante inteligencia artificial, construye un contexto unificado y genera una nueva nota periodística en formato estructurado.

Este proyecto fue desarrollado como iniciativa personal y constituye el backend de una plataforma actualmente en desarrollo orientada a la automatización de portales de noticias.

## Objetivos

* Automatizar la búsqueda de noticias en medios digitales.
* Construir contexto a partir de múltiples fuentes de información.
* Generar contenido periodístico utilizando modelos de lenguaje (LLM).
* Exponer todas las funcionalidades mediante una API REST.
* Diseñar una arquitectura modular que facilite su evolución hacia una plataforma basada en microservicios.



## Características

- Obtención automática de noticias desde Google News RSS.
- Resolución de enlaces de Google News hacia la URL original del medio.
- Extracción del contenido periodístico mediante Web Scraping.
- Soporte para sitios protegidos utilizando Playwright como mecanismo alternativo.
- Selección automática de las noticias más relevantes utilizando un LLM.
- Generación de una noticia completamente nueva basada en múltiples fuentes.
- Generación automática de título y resumen.
- Obtención de imágenes relacionadas mediante Unsplash.
- Fallback automático hacia Pollinations cuando Unsplash no devuelve resultados.
- API REST desarrollada con FastAPI.


## Flujo de funcionamiento

```text
                Query
                  │
                  ▼
          Google News RSS
                  │
                  ▼
      Resolución de URLs reales
                  │
                  ▼
        Scraping del contenido
      (Requests / Playwright)
                  │
                  ▼
      Selección de noticias
            más relevantes
            (Groq LLM)
                  │
                  ▼
      Generación de noticia
            (Groq LLM)
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   Resumen             Título y Texto
        │
        ▼
 Búsqueda de imágenes
(Unsplash → Pollinations)
        │
        ▼
      Respuesta JSON
```


# Funcionalidades

NEWS-GEN-LLM expone una API REST orientada a la automatización de contenido periodístico mediante técnicas de Web Scraping y Large Language Models (LLM). Actualmente dispone de tres servicios principales que pueden utilizarse de forma independiente o como parte de un flujo completo de generación de noticias.

---

## Generación automática de noticias

**Endpoint**

```http
POST /generar-noticia
```

Genera una noticia completamente nueva a partir de una consulta (`query`).

### Flujo de procesamiento

1. Obtiene noticias relacionadas mediante el endpoint interno de scraping.
2. Envía todas las noticias recuperadas a un LLM para identificar cuáles son las más relevantes para la consulta.
3. Utiliza únicamente esas noticias como contexto para una segunda llamada al LLM, encargada de redactar una noticia completamente nueva.
4. Genera un resumen corto en formato `palabra1_palabra2_palabra3`.
5. Utiliza dicho resumen como consulta para obtener imágenes relacionadas.
6. Devuelve un único objeto JSON con el contenido generado.

### Respuesta

```json
{
  "titulo": "Título generado",
  "texto": "Contenido completo de la noticia...",
  "resumen": "palabra1_palabra2_palabra3",
  "imagenes": [
    "https://...",
    "https://..."
  ]
}
```

---

## Obtención de imágenes

**Endpoint**

```http
POST /imagenes
```

Obtiene imágenes relacionadas con una consulta.

### Funcionamiento

El servicio implementa una estrategia de *fallback* entre múltiples proveedores:

1. Consulta inicialmente la API de **Unsplash**.
2. Si Unsplash no responde o no devuelve resultados válidos, utiliza **Pollinations** como proveedor alternativo.

### Respuesta

```json
[
    "https://imagen1.jpg",
    "https://imagen2.jpg"
]
```

---

## Scraping de noticias

**Endpoint**

```http
POST /scrape-noticias
```

Obtiene noticias recientes relacionadas con una consulta de búsqueda.

### Flujo de procesamiento

El proceso de scraping consta de varias etapas para maximizar la calidad del contenido obtenido:

1. Consulta Google News RSS utilizando la consulta recibida.
2. Extrae los enlaces mediante BeautifulSoup.
3. Resuelve las URL de redirección de Google News hasta obtener la URL real del medio periodístico.
4. Descarga el contenido utilizando `requests`.
5. Si el sitio bloquea el acceso (por ejemplo, mediante un **HTTP 403**), intenta nuevamente utilizando **Playwright** para renderizar la página como un navegador real.
6. Limpia el HTML eliminando scripts, estilos y contenido irrelevante.
7. Extrae únicamente el texto útil de la noticia.

### Respuesta

```json
[
    {
        "titulo": "...",
        "url": "...",
        "texto": "..."
    }
]
```

---

## Arquitectura del flujo principal

```
Query
  │
  ▼
Scraping de noticias
  │
  ▼
Google News RSS
  │
  ▼
Noticias obtenidas
  │
  ▼
LLM (selección de noticias relevantes)
  │
  ▼
Noticias relevantes
  │
  ▼
LLM (redacción periodística)
  │
  ▼
Título + Texto + Resumen
  │
  ▼
Scraping de imágenes
  │
  ▼
Unsplash
     └── si falla → Pollinations
  │
  ▼
Respuesta JSON final
```


Instalación
Requisitos
Python 3.12 o superior
Google Chrome / Chromium (Playwright)
Cuenta y API Key de Groq
API Key de Unsplash
Clonar el repositorio
git clone https://github.com/TU-USUARIO/NEWS-GEN-LLM.git

cd NEWS-GEN-LLM
Crear un entorno virtual

Linux

python -m venv v-news-llm

source v-news-llm/bin/activate

Windows

python -m venv v-news-llm

v-news-llm\Scripts\activate
Instalar dependencias
pip install -r requirements.txt
Instalar Playwright
playwright install chromium

Después vendría la sección de Configuración, porque tu proyecto depende de varias API Keys.

Configuración

El proyecto utiliza variables de entorno para almacenar credenciales y parámetros sensibles.

Crear un archivo .env con el siguiente contenido:

GROQ_API_KEY=xxxxxxxxxxxxxxxxxxxx

UNSPLASH_API_KEY=xxxxxxxxxxxxxxxxxxxx

Si se desean utilizar proveedores adicionales de imágenes o motores de búsqueda, las credenciales pueden incorporarse siguiendo la misma estructura.

Luego agregaría cómo levantar el servidor.

Ejecución

Iniciar la API con:

uvicorn app.main:app --reload

