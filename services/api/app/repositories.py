from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from .models import StockPrice

class PriceReadRepository:
    def latest(self, s: Session, symbol: str):
        stmt = select(StockPrice).where(StockPrice.symbol == symbol).order_by(desc(StockPrice.datetime)).limit(1)
        return s.execute(stmt).scalars().first()

    def last_n(self, s: Session, symbol: str, n: int):
        stmt = select(StockPrice).where(StockPrice.symbol == symbol).order_by(desc(StockPrice.datetime)).limit(n)
        return list(s.execute(stmt).scalars())
