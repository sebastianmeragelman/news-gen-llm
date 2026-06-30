
from app.services.news_service import generar_noticia


def test_generar_noticia_integracion():

    resultado = generar_noticia(
        query="cordoba deportes",
        max_links=5,
        cant_imagenes=3
    )

    # ------------------------------------------------
    # Validación estructura general
    # ------------------------------------------------

    assert isinstance(resultado, dict), "La respuesta debe ser un diccionario"

    assert "titulo" in resultado
    assert "texto" in resultado
    assert "resumen" in resultado
    assert "imagenes" in resultado

    # ------------------------------------------------
    # TÍTULO
    # ------------------------------------------------

    assert isinstance(resultado["titulo"], str)

    titulo = resultado["titulo"].strip()

    assert len(titulo) > 0

    palabras = titulo.split()

    assert 2 <= len(palabras) <= 10, \
        f"Título inválido ({len(palabras)} palabras)"

    # ------------------------------------------------
    # TEXTO
    # ------------------------------------------------

    assert isinstance(resultado["texto"], str)

    texto = resultado["texto"].strip()

    palabras_texto = texto.split()

    assert 300 <= len(palabras_texto) <= 600, \
        f"Texto inválido ({len(palabras_texto)} palabras)"

    # ------------------------------------------------
    # RESUMEN
    # ------------------------------------------------

    assert isinstance(resultado["resumen"], str)

    resumen = resultado["resumen"].strip()

    elementos = resumen.split("_")

    assert 3 <= len(elementos) <= 6, \
        f"Resumen inválido ({len(elementos)} términos)"

    for palabra in elementos:
        assert len(palabra) > 0

    # ------------------------------------------------
    # IMÁGENES
    # ------------------------------------------------

    assert isinstance(resultado["imagenes"], list)

    assert len(resultado["imagenes"]) == 3

    for url in resultado["imagenes"]:

        assert isinstance(url, str)

        assert url.startswith("http"), \
            f"URL inválida: {url}"
