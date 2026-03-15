from app.orchestrator import MarketAnalysisOrchestrator
from app.schemas import AnalysisRequest, WebResearchResult


def test_orchestrator_returns_complete_response(monkeypatch):
    orchestrator = MarketAnalysisOrchestrator()

    mock_web_research = {
        "query": "iPhone 16 market price competitors reviews US",
        "findings": [
            {
                "title": "iPhone 16 vs Samsung Galaxy S24",
                "snippet": "The iPhone 16 starts at $799 and competes with the Galaxy S24.",
                "link": "https://example.com/article1",
            }
        ],
    }

    mock_insights = {
        "pricing_context": "The iPhone 16 starts at $799.",
        "key_competitors": ["Samsung Galaxy S24"],
        "customer_sentiment": "Customer perception appears generally positive.",
        "market_trend": "Competition remains strong in the premium smartphone segment.",
        "confidence_note": "Based on limited retrieved evidence.",
    }

    mock_report = "This is a generated market report."
    mock_path = "reports/iphone_16_us_test.json"

    monkeypatch.setattr(
        orchestrator.web_research_tool,
        "run",
        lambda product_name, region: WebResearchResult(**mock_web_research)
    )

    monkeypatch.setattr(
        "app.orchestrator.extract_market_insights",
        lambda product_name, region, research_results: mock_insights
    )

    monkeypatch.setattr(
        "app.orchestrator.generate_market_report",
        lambda product_name, region, insights, sources: mock_report
    )

    monkeypatch.setattr(
        orchestrator.report_store,
        "save",
        lambda product_name, region, report: mock_path
    )

    request = AnalysisRequest(
        product_name="iPhone 16",
        region="US",
        user_query="Generate a market analysis report",
    )

    result = orchestrator.run(request)

    assert result.product_name == "iPhone 16"
    assert result.region == "US"
    assert result.report == mock_report
    assert result.stored_at == mock_path
    assert result.extracted_insights.pricing_context == "The iPhone 16 starts at $799."
    assert result.extracted_insights.key_competitors == ["Samsung Galaxy S24"]