from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analyze_endpoint_success(monkeypatch):
    from app.routes import orchestrator

    mock_response = {
        "product_name": "iPhone 16",
        "region": "US",
        "plan": {
            "tools": ["web_research", "insight_extraction", "report_generation"],
            "reasoning": "The agent will retrieve web evidence, extract structured market insights from that evidence, and generate a market report.",
        },
        "web_research": {
            "query": "iPhone 16 market price competitors reviews US",
            "findings": [
                {
                    "title": "iPhone 16 vs Samsung Galaxy S24",
                    "snippet": "The iPhone 16 starts at $799.",
                    "link": "https://example.com/article1",
                }
            ],
        },
        "extracted_insights": {
            "pricing_context": "The iPhone 16 starts at $799.",
            "key_competitors": ["Samsung Galaxy S24"],
            "customer_sentiment": "Customer perception appears generally positive.",
            "market_trend": "Competition remains strong in the premium smartphone segment.",
            "confidence_note": "Based on limited retrieved evidence.",
        },
        "report": "Generated report",
        "stored_at": "reports/test.json",
    }

    monkeypatch.setattr(
        orchestrator,
        "run",
        lambda request: type("MockResponse", (), mock_response)()
    )

    response = client.post(
        "/analyze",
        json={
            "product_name": "iPhone 16",
            "region": "US",
            "user_query": "Generate a market analysis report",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["product_name"] == "iPhone 16"
    assert body["region"] == "US"
    assert "report" in body


def test_analyze_endpoint_validation_error():
    response = client.post(
        "/analyze",
        json={
            "product_name": "",
            "region": "US",
            "user_query": "Generate a market analysis report",
        },
    )

    assert response.status_code == 400