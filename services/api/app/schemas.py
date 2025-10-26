from pydantic import BaseModel


class LatestResponse(BaseModel):
    symbol: str
    datetime: str
    close: float


class TrendResponse(BaseModel):
    symbol: str
    latest_close: float
    change_pct: float
    ma_7: float | None
    volatility_7: float | None
    observations: int
