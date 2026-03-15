import os

import requests
from dotenv import load_dotenv

from app.schemas import WebResearchResult

load_dotenv()


class WebResearchTool:
    def __init__(self) -> None:
        self.url = "https://google.serper.dev/search"

    def run(self, product_name: str, region: str) -> WebResearchResult:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            raise ValueError("SERPER_API_KEY is not set")

        query = f"{product_name} vs competitors alternatives similar products {region}"

        response = requests.post(
            self.url,
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json",
            },
            json={
                "q": query,
                "num": 5,
            },
            timeout=20,
        )

        response.raise_for_status()
        data = response.json()

        organic_results = data.get("organic", [])

        findings = []
        for item in organic_results[:5]:
            findings.append(
                {
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", ""),
                }
            )

        if not findings:
            findings.append(
                {
                    "title": f"No direct search results for {product_name}",
                    "snippet": f"No organic results were returned for {product_name} in {region}.",
                    "link": "",
                }
            )

        return WebResearchResult(query=query, findings=findings)
