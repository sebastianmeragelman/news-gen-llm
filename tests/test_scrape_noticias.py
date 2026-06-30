from app.services.scraper_noticias import obtener_noticias

def test_scrape_noticias():
    data = obtener_noticias("cordoba deportes", 5)

    assert hasattr(data, "noticias")
    assert isinstance(data.noticias, list) , "data.noticias no es una lista"
    assert len(data.noticias) <= 5 , "data.noticias devolvio mas url que las pedidas"


    for item in data.noticias:
        assert isinstance(item, dict) , "data.noticias no es un diccionario"
        assert "titulo" in item , "no devolvio titulo"
        assert "url" in item , "no devolvio url"
        assert "texto" in item , "no devolvio titulo"


        assert isinstance(item["titulo"], str)
        assert isinstance(item["url"], str)
        assert isinstance(item["texto"], str)
        assert len(item["texto"]) > 0        
        assert item["url"].startswith("http") , "la url no comienza con http"