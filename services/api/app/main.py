from fastapi import FastAPI, Query
from statistics import pstdev
from .db import session_scope
from .repositories import PriceReadRepository
from .schemas import LatestResponse, TrendResponse

app = FastAPI(title="Twelve Insight API")

@app.get("/health")
def health(): return {"status": "ok"}

@app.get("/latest", response_model=LatestResponse)
def latest(ticker: str = Query(...)):
    repo = PriceReadRepository()
    with session_scope() as s:
        rec = repo.latest(s, ticker)
    if not rec:
        return {"symbol": ticker, "datetime": "", "close": 0.0}
    return {"symbol": rec.symbol, "datetime": rec.datetime.isoformat(), "close": rec.close}

@app.get("/trend", response_model=TrendResponse)
def trend(ticker: str = Query(...), window: int = 100):
    repo = PriceReadRepository()
    with session_scope() as s:
        rows = list(reversed(repo.last_n(s, ticker, window)))
    if len(rows) < 2:
        return {"symbol": ticker, "latest_close": 0.0, "change_pct": 0.0, "ma_7": 0.0, "volatility_7": 0.0, "observations": len(rows)}
    closes = [r.close for r in rows]
    latest, prev = closes[-1], closes[-2]
    change = ((latest - prev) / prev) * 100 if prev else 0
    window7 = closes[-7:] if len(closes) >= 7 else closes
    return {
        "symbol": ticker,
        "latest_close": latest,
        "change_pct": change,
        "ma_7": sum(window7) / len(window7),
        "volatility_7": pstdev(window7) if len(window7) > 1 else 0.0,
        "observations": len(closes),
    }
