from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import StockPrice

class PriceRepository:
    def latest_dt(self, session: Session, symbol: str):
        stmt = select(StockPrice.datetime).where(StockPrice.symbol == symbol).order_by(StockPrice.datetime.desc()).limit(1)
        row = session.execute(stmt).first()
        return row[0] if row else None

    def bulk_insert(self, session: Session, symbol: str, values: list[dict]) -> int:
        objs = [
            StockPrice(
                symbol=symbol,
                datetime=v["datetime"],
                open=float(v["open"]),
                high=float(v["high"]),
                low=float(v["low"]),
                close=float(v["close"]),
                volume=float(v["volume"]) if v.get("volume") else None,
            )
            for v in values
        ]
        session.bulk_save_objects(objs)
        return len(objs)
