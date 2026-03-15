PRODUCT_PRICE_DATA = {
    "nike air max": {
        "US": [
            {"source": "Amazon", "price": 129.99, "availability": "in_stock"},
            {"source": "Walmart", "price": 124.99, "availability": "in_stock"},
            {"source": "Target", "price": 134.99, "availability": "limited"},
        ]
    },
    "iphone 15": {
        "US": [
            {"source": "Amazon", "price": 799.00, "availability": "in_stock"},
            {"source": "Best Buy", "price": 829.00, "availability": "in_stock"},
            {"source": "Walmart", "price": 809.00, "availability": "limited"},
        ]
    },
}

PRODUCT_REVIEWS = {
    "nike air max": [
        "Very comfortable and looks great.",
        "Good quality overall but a bit expensive.",
        "Comfort is excellent for daily use.",
        "Nice design, but the price feels high.",
    ],
    "iphone 15": [
        "Excellent camera and smooth performance.",
        "Battery life is decent but not amazing.",
        "Very fast and reliable.",
        "Good phone, but expensive for the upgrade.",
    ],
}

PRODUCT_TRENDS = {
    "nike air max": {
        "US": {
            "price_trend": "stable",
            "demand_trend": "increasing",
            "seasonality_note": "Demand tends to improve during spring promotions."
        }
    },
    "iphone 15": {
        "US": {
            "price_trend": "decreasing",
            "demand_trend": "stable",
            "seasonality_note": "Prices usually soften as newer models approach."
        }
    },
}
