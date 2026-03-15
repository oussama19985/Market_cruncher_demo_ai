import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _get_client() -> OpenAI:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )


def extract_market_insights(
    product_name: str,
    region: str,
    research_results: list[dict],
) -> dict:
    client = _get_client()

    evidence = "\n".join(
        f"- {item.get('title', '')}: {item.get('snippet', '')}"
        for item in research_results
    )

    prompt = f"""
You are a market research analyst.

Product: {product_name}
Region: {region}

Using ONLY the evidence below, extract structured market insights.

Evidence:
{evidence}

Return ONLY valid JSON with this structure:

{{
  "pricing_context": "...",
  "key_competitors": ["..."],
  "customer_sentiment": "...",
  "market_trend": "...",
  "confidence_note": "..."
}}

Rules:
- Do NOT invent facts
- Use only the evidence provided
- Competitors should be from other companies when possible
- Avoid listing variants from the same product line as competitors
- If evidence is weak, say so clearly in confidence_note
- No markdown
- No explanation outside the JSON
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a careful market analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content or ""
    content = re.sub(r"```json|```", "", content).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned invalid JSON:\n{content}") from exc


def generate_market_report(
    product_name: str,
    region: str,
    insights: dict,
    sources: list[str],
) -> str:
    client = _get_client()

    source_list = (
        "\n".join(f"- {source}" for source in sources)
        if sources
        else "- No source domains available"
    )

    prompt = f"""
Write a concise professional market analysis report.

Product: {product_name}
Region: {region}

Insights:
{json.dumps(insights, indent=2)}

Write the report with these sections:
1. Pricing context
2. Key competitors
3. Customer perception
4. Market trend
5. Strategic recommendation

End the report with a Sources section listing exactly these domains:

{source_list}

Rules:
- Stay grounded in the provided insights
- Do not invent facts
- Do not invent sources
- If confidence is limited, make that clear in the report
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You write professional market research reports.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content or ""
