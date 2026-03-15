from pydantic import BaseModel
from typing import List, Optional, Dict


class AnalysisRequest(BaseModel):
    product_name: str
    region: str
    user_query: str


class AnalysisPlanResponse(BaseModel):
    tools: List[str]
    reasoning: str


class WebResearchResult(BaseModel):
    query: str
    findings: List[Dict[str, str]]


class ExtractedInsights(BaseModel):
    pricing_context: str
    key_competitors: List[str]
    customer_sentiment: str
    market_trend: str
    confidence_note: str


class AnalysisResponse(BaseModel):
    product_name: str
    region: str
    plan: AnalysisPlanResponse
    web_research: Optional[WebResearchResult] = None
    extracted_insights: ExtractedInsights
    report: str
    stored_at: str
