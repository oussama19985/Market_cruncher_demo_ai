from app.schemas import ExtractedInsights


def build_markdown_report(
    product_name: str,
    region: str,
    extracted_insights: ExtractedInsights,
    report_text: str,
    sentiment_chart_filename: str,
    competitor_chart_filename: str,
    sources: list[str],
) -> str:
    source_lines = (
        "\n".join(f"- {source}" for source in sources)
        if sources
        else "- No sources available"
    )

    markdown = f"""# Market Analysis Report

**Product:** {product_name}  
**Region:** {region}

---

## Executive Summary

{report_text}

---

## Structured Insights

### Pricing Context
{extracted_insights.pricing_context}

### Key Competitors
{", ".join(extracted_insights.key_competitors) if extracted_insights.key_competitors else "No clear competitors identified."}

### Customer Sentiment
{extracted_insights.customer_sentiment}

### Market Trend
{extracted_insights.market_trend}

### Confidence Note
{extracted_insights.confidence_note}

---

## Visualizations

### Customer Sentiment Overview
![Sentiment Chart]({sentiment_chart_filename})

### Competitor Overview
![Competitor Chart]({competitor_chart_filename})

---

## Sources

{source_lines}
"""
    return markdown
