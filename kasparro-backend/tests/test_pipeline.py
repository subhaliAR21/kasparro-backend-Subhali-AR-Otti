import pytest
from schemas.price import PriceSchema
from datetime import datetime

def test_price_schema_validation():
    # Test if our unified schema correctly validates data
    data = {
        "source": "test_source",
        "asset": "BTC",
        "price_usd": 50000.0,
        "timestamp": datetime.utcnow()
    }
    schema = PriceSchema(**data)
    assert schema.source == "test_source"
    assert schema.price_usd == 50000.0