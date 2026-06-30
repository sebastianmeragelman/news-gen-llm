import requests

from app.scrapers.image_unsplash import obtener_imagenes_unsplash


def test_unsplash_integracion():

    imagenes = obtener_imagenes_unsplash(
        query="cordoba argentina",
        per_page=3
    )

    # -------------------------
    # Validación del retorno
    # -------------------------

    assert isinstance(imagenes, list), "No devolvió una lista"

    assert len(imagenes) > 0, "No se obtuvieron imágenes"

    # -------------------------
    # Validación de cada imagen
    # -------------------------

    for url in imagenes:

        assert isinstance(url, str), "La URL no es string"

        assert url.startswith("http"), "URL inválida"

        response = requests.get(url, timeout=20)

        assert response.status_code == 200, (
            f"La imagen respondió {response.status_code}"
        )

        content_type = response.headers.get("Content-Type", "")

        assert content_type.startswith("image"), (
            f"No es una imagen ({content_type})"
        )

        tamaño = len(response.content)

        assert tamaño > 15 * 1024, (
            f"La imagen pesa solo {tamaño} bytes"
        )

        assert len(imagenes) == 3