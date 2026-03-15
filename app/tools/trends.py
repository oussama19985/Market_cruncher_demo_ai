from app.schemas import TrendResult


class TrendAnalyzerTool:
    def run(self, product_name: str, region: str) -> TrendResult:
        product_key = product_name.strip().lower()

        if "iphone" in product_key:
            return TrendResult(
                price_trend="decreasing",
                demand_trend="stable",
                market_note=f"Prices in {region} may soften as newer product cycles approach.",
            )

        if "nike" in product_key:
            return TrendResult(
                price_trend="stable",
                demand_trend="increasing",
                market_note=f"Demand in {region} appears supported by seasonal promotions and brand strength.",
            )

        return TrendResult(
            price_trend="stable",
            demand_trend="stable",
            market_note=f"Market signal for {product_name} in {region} is limited, but appears broadly stable.",
        )
