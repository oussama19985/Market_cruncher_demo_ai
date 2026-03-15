from urllib.parse import urlparse

from app.planner import AnalysisPlanner
from app.report_store import ReportStore
from app.report_formatter import build_markdown_report
from app.visualizations import ReportVisualizer
from app.schemas import (
    AnalysisPlanResponse,
    AnalysisRequest,
    AnalysisResponse,
    ExtractedInsights,
    WebResearchResult,
)
from app.tools.web_research import WebResearchTool
from app.llm_client import extract_market_insights, generate_market_report


class MarketAnalysisOrchestrator:
    """
    Orchestrates the market analysis workflow.

    Flow:
    1. Build an execution plan
    2. Retrieve web evidence
    3. Extract structured insights from evidence using the LLM
    4. Generate the final market report using the LLM
    5. Generate visualizations
    6. Save report artifacts
    """

    def __init__(self) -> None:
        self.planner = AnalysisPlanner()
        self.web_research_tool = WebResearchTool()
        self.report_store = ReportStore()
        self.visualizer = ReportVisualizer()

    def run(self, request: AnalysisRequest) -> AnalysisResponse:
        product_name = request.product_name.strip()
        region = request.region.strip()
        user_query = request.user_query.strip()

        if not product_name:
            raise ValueError("product_name cannot be empty")

        if not region:
            raise ValueError("region cannot be empty")

        plan = self.planner.build_plan(user_query)

        web_research: WebResearchResult | None = None

        for tool_name in plan.tools:
            if tool_name == "web_research":
                web_research = self.web_research_tool.run(product_name, region)

        if web_research is None:
            raise ValueError("Web research failed — no evidence retrieved")

        insights_dict = extract_market_insights(
            product_name=product_name,
            region=region,
            research_results=web_research.findings,
        )

        extracted_insights = ExtractedInsights(**insights_dict)

        sources = sorted(
            {
                urlparse(item["link"]).netloc
                for item in web_research.findings
                if item.get("link")
            }
        )

        report = generate_market_report(
            product_name=product_name,
            region=region,
            insights=insights_dict,
            sources=sources,
        )

        base_filename = self.report_store.build_base_filename(
            product_name=product_name,
            region=region,
        )

        sentiment_chart_path = self.visualizer.generate_sentiment_chart(
            base_filename=base_filename,
            sentiment_text=extracted_insights.customer_sentiment,
        )

        competitor_chart_path = self.visualizer.generate_competitor_chart(
            base_filename=base_filename,
            competitors=extracted_insights.key_competitors,
        )

        sentiment_chart_filename = sentiment_chart_path.split("/")[-1]
        competitor_chart_filename = competitor_chart_path.split("/")[-1]

        markdown_report = build_markdown_report(
            product_name=product_name,
            region=region,
            extracted_insights=extracted_insights,
            report_text=report,
            sentiment_chart_filename=sentiment_chart_filename,
            competitor_chart_filename=competitor_chart_filename,
            sources=sources,
        )

        json_payload = {
            "product_name": product_name,
            "region": region,
            "plan": {
                "tools": plan.tools,
                "reasoning": plan.reasoning,
            },
            "web_research": web_research.model_dump(),
            "extracted_insights": extracted_insights.model_dump(),
            "report": report,
            "sources": sources,
            "artifacts": {
                "sentiment_chart": sentiment_chart_filename,
                "competitor_chart": competitor_chart_filename,
            },
        }

        stored_at = self.report_store.save_json(
            base_filename=base_filename,
            payload=json_payload,
        )

        self.report_store.save_markdown(
            base_filename=base_filename,
            content=markdown_report,
        )

        return AnalysisResponse(
            product_name=product_name,
            region=region,
            plan=AnalysisPlanResponse(
                tools=plan.tools,
                reasoning=plan.reasoning,
            ),
            web_research=web_research,
            extracted_insights=extracted_insights,
            report=report,
            stored_at=stored_at,
        )
