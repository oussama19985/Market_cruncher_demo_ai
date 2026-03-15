from app.tools.web_research import WebResearchTool


def test_web_research_returns_results(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "organic": [
                    {
                        "title": "Test title",
                        "snippet": "Test snippet",
                        "link": "https://example.com",
                    }
                ]
            }

    monkeypatch.setattr(
        "app.tools.web_research.requests.post",
        lambda *args, **kwargs: MockResponse()
    )

    monkeypatch.setenv("SERPER_API_KEY", "fake_key")

    tool = WebResearchTool()
    result = tool.run("iPhone 16", "US")

    assert result.query == "iPhone 16 market price competitors reviews US"
    assert len(result.findings) == 1
    assert result.findings[0]["title"] == "Test title"