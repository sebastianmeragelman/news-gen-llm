import requests
from app.scrapers.image_unsplash import obtener_imagenes_unsplash


# -------------------------
# Fake response de Unsplash
# -------------------------
class FakeResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code

    def json(self):
        return {
            "results": [
                {
                    "urls": {
                        "regular": "https://img1.jpg"
                    }
                },
                {
                    "urls": {
                        "regular": "https://img2.jpg"
                    }
                },
                {
                    "urls": {
                        "regular": "https://img3.jpg"
                    }
                }
            ]
        }


# -------------------------
# Mock de requests.get
# -------------------------
def fake_requests_get(*args, **kwargs):
    return FakeResponse(200)


# -------------------------
# TEST PRINCIPAL
# -------------------------
def test_obtener_imagenes_unsplash(monkeypatch):

    # reemplazamos requests.get por fake
    monkeypatch.setattr(requests, "get", fake_requests_get)

    result = obtener_imagenes_unsplash(
        query="cordoba deportes",
        per_page=3
    )

    # -------------------------
    # VALIDACIONES
    # -------------------------
    assert isinstance(result, list), "La respuesta no es una lista"
    assert len(result) == 3, "No devolvió la cantidad esperada"

    for url in result:
        assert isinstance(url, str), "Elemento no es string"
        assert url.startswith("https://"), "URL inválida"



    