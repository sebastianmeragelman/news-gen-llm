from app.services.scraper_noticias import obtener_noticias

def test_scrape_noticias():
    data = obtener_noticias("cordoba deportes", 5)

    assert isinstance(data, list)
    assert len(data) == 5


    for item in data:
        assert isinstance(item, dict)
        assert "titulo" in item
        assert "url" in item
        assert "texto" in item


        assert isinstance(item["titulo"], str)
        assert isinstance(item["url"], str)
        assert isinstance(item["texto"], str)

        assert item["url"].startswith("http")