from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PriceSchema(BaseModel):
    source: str
    asset: str
    price_usd: float
    timestamp: datetime = datetime.utcnow()