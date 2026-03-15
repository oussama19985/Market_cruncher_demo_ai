from dataclasses import dataclass
from typing import List


@dataclass
class AnalysisPlan:
    tools: List[str]
    reasoning: str


class AnalysisPlanner:
    """
    Responsible for deciding which tools the agent should run
    to satisfy the user's request.
    """

    def build_plan(self, user_query: str) -> AnalysisPlan:
        request = user_query.lower()

        # Default pipeline for any analysis request
        tools = [
            "web_research",
            "insight_extraction",
            "report_generation",
        ]

        # Reasoning logic (lightweight — no heuristics about sentiment/trends)
        if any(word in request for word in ["report", "analysis", "analyze"]):
            reasoning = (
                "The agent will retrieve web evidence, extract structured market "
                "insights from that evidence, and generate a market report."
            )

        elif any(word in request for word in ["price", "competitor", "market"]):
            reasoning = (
                "The agent will retrieve market data from the web, extract pricing "
                "and competitive insights, and summarize the findings."
            )

        else:
            reasoning = (
                "The request is general, so the agent will perform web research, "
                "extract insights from the evidence, and produce a report."
            )

        return AnalysisPlan(
            tools=tools,
            reasoning=reasoning,
        )
