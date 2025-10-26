import logging, time
from .client import TwelveDataClient
from .repositories import PriceRepository
from .db import session_scope
from .config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("collector")

def backfill():
    client = TwelveDataClient()
    repo = PriceRepository()
    for sym in settings.symbols_list:
        with session_scope() as s:
            latest = repo.latest_dt(s, sym)
        if latest:
            logger.info("Already have data for %s, skip full backfill.", sym)
            continue
        values = client.fetch_time_series(sym)
        with session_scope() as s:
            repo.bulk_insert(s, sym, values)
        logger.info("Backfilled %d rows for %s", len(values), sym)

def collect_once():
    client = TwelveDataClient()
    repo = PriceRepository()
    for sym in settings.symbols_list:
        latest_pt = client.fetch_latest(sym)
        if not latest_pt:
            continue
        with session_scope() as s:
            current = repo.latest_dt(s, sym)
        if not current or str(current) < latest_pt["datetime"]:
            with session_scope() as s:
                repo.bulk_insert(s, sym, [latest_pt])
            logger.info("Inserted new datapoint for %s (%s)", sym, latest_pt["datetime"])
        else:
            logger.info("No update for %s", sym)

def run():
    backfill()
    while True:
        collect_once()
        time.sleep(settings.COLLECT_INTERVAL_SECONDS)
