import os
import requests
from dotenv import load_dotenv
from app.schemas import WebResearchResult

load_dotenv()


class WebResearchTool:
    def __init__(self) -> None:
        self.api_key = os.getenv("SERPER_API_KEY")

        if not self.api_key:
            raise ValueError("SERPER_API_KEY is not set")

        self.url = "https://google.serper.dev/search"

    def run(self, product_name: str, region: str) -> WebResearchResult:
        query = f"{product_name} market price competitors reviews {region}"

        response = requests.post(
            self.url,
            headers={
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
            },
            json={"q": query, "num": 5},
            timeout=20,
        )

        response.raise_for_status()
        data = response.json()

        findings = []
        for item in data.get("organic", [])[:5]:
            findings.append(
                {
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", ""),
                }
            )

        return WebResearchResult(query=query, findings=findings)
