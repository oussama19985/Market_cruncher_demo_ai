from app.schemas import SentimentResult


class SentimentAnalyzerTool:
    def run(self, product_name: str, region: str | None = None) -> SentimentResult:
        product_key = product_name.strip().lower()

        if "iphone" in product_key:
            return SentimentResult(
                overall_sentiment="mixed",
                positives=[
                    "Users often highlight camera quality.",
                    "Performance is generally seen as a strong point.",
                ],
                negatives=[
                    "Price is a recurring concern.",
                    "Battery life receives mixed feedback.",
                ],
            )

        if "nike" in product_key:
            return SentimentResult(
                overall_sentiment="positive",
                positives=[
                    "Customers often mention comfort.",
                    "Design is generally appreciated.",
                ],
                negatives=[
                    "Price is sometimes seen as high.",
                ],
            )

        return SentimentResult(
            overall_sentiment="mixed",
            positives=[
                f"There are some positive signals around perceived value for {product_name}.",
            ],
            negatives=[
                f"There is not enough high-confidence review evidence for {product_name}.",
            ],
        )
