import os
import logging
from sqlalchemy.orm import Session
from services.collector.app.db import SessionLocal, init_db
from services.collector.app.collector import TwelveDataClient

def main():
    logging.basicConfig(level=logging.INFO)
    symbols = ["AAPL", "TSLA", "BTC/USD"]
    api_key = os.getenv("TWELVEDATA_API_KEY")

    init_db()
    client = TwelveDataClient(api_key=api_key, symbols=symbols)
    db: Session = SessionLocal()

    for symbol in symbols:
        data = client.fetch_historical_data(symbol)
        if data:
            client.save_to_db(db, symbol, data)
            logging.info(f"Inserted {len(data)} records for {symbol}")

if __name__ == "__main__":
    main()
