from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


class ReportVisualizer:
    def __init__(self) -> None:
        self.base_dir = Path("reports")
        self.base_dir.mkdir(exist_ok=True)

    def generate_sentiment_chart(self, base_filename: str, sentiment_text: str) -> str:
        """
        Very simple mapping only for visualization.
        We are not using this to compute sentiment, only to display it.
        """
        sentiment_lower = sentiment_text.lower()

        if "positive" in sentiment_lower:
            values = [7, 2, 1]
        elif "negative" in sentiment_lower:
            values = [1, 2, 7]
        else:
            values = [4, 3, 3]

        labels = ["Positive", "Neutral", "Negative"]

        output_path = self.base_dir / f"{base_filename}_sentiment.png"

        plt.figure(figsize=(6, 4))
        plt.bar(labels, values)
        plt.title("Customer Sentiment Overview")
        plt.ylabel("Relative signal")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return str(output_path)

    def generate_competitor_chart(
        self,
        base_filename: str,
        competitors: list[str],
    ) -> str:
        """
        Creates a simple competitor presence chart.
        Since we do not have exact competitor prices yet,
        we visualize competitor mentions uniformly.
        """
        if not competitors:
            competitors = ["No clear competitors found"]

        values = [1 for _ in competitors]

        output_path = self.base_dir / f"{base_filename}_competitors.png"

        plt.figure(figsize=(8, 4))
        plt.bar(competitors, values)
        plt.title("Key Competitors Identified")
        plt.ylabel("Presence in extracted insights")
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        return str(output_path)
