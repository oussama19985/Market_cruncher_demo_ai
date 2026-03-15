from app.schemas import CompetitorPrice, ProductResearchResult
from app.tools.mock_data import PRODUCT_PRICE_DATA


class ProductResearchTool:
    def run(self, product_name: str, market: str) -> ProductResearchResult:
        key = product_name.strip().lower()

        if key not in PRODUCT_PRICE_DATA or market not in PRODUCT_PRICE_DATA[key]:
            raise ValueError(
                f"No product research data available for '{product_name}' in market '{market}'"
            )

        raw_competitors = PRODUCT_PRICE_DATA[key][market]
        competitors = [CompetitorPrice(**item) for item in raw_competitors]
        average_price = round(
            sum(item.price for item in competitors) / len(competitors), 2
        )

        return ProductResearchResult(
            average_price=average_price,
            competitors=competitors,
        )
