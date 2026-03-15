from app.schemas import WebResearchResult, SentimentResult, TrendResult


class ReportGenerator:
    def generate(
        self,
        product_name: str,
        region: str,
        web_research: WebResearchResult | None,
        sentiment: SentimentResult | None,
        trend: TrendResult | None,
    ) -> str:
        lines = []
        lines.append(f"Market Analysis Report - {product_name} ({region})")
        lines.append("")

        if web_research is not None:
            lines.append("Market Research")
            for finding in web_research.findings:
                lines.append(f"- {finding['title']}: {finding['snippet']}")
            lines.append("")

        if sentiment is not None:
            lines.append("Customer Sentiment")
            lines.append(f"- Overall sentiment: {sentiment.overall_sentiment}")
            if sentiment.positives:
                lines.append("- Positive themes:")
                for item in sentiment.positives:
                    lines.append(f"  - {item}")
            if sentiment.negatives:
                lines.append("- Negative themes:")
                for item in sentiment.negatives:
                    lines.append(f"  - {item}")
            lines.append("")

        if trend is not None:
            lines.append("Market Trends")
            lines.append(f"- Price trend: {trend.price_trend}")
            lines.append(f"- Demand trend: {trend.demand_trend}")
            lines.append(f"- Note: {trend.market_note}")
            lines.append("")

        lines.append("Recommendation")
        lines.append(
            f"- {product_name} in {region} appears to require positioning that balances customer perception, market demand, and competitive context."
        )

        return "\n".join(lines)
