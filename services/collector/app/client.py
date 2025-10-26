import requests, logging
from typing import List, Dict, Optional
from .config import settings

logger = logging.getLogger(__name__)


class TwelveDataClient:
    BASE_URL = "https://api.twelvedata.com/time_series"

    def __init__(self):
        self.api_key = settings.TWELVEDATA_API_KEY

    def fetch_time_series(self, symbol: str) -> List[Dict]:
        params = {
            "symbol": symbol,
            "interval": settings.INTERVAL,
            "outputsize": settings.OUTPUTSIZE,
            "apikey": self.api_key,
        }
        r = requests.get(self.BASE_URL, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        return list(reversed(data.get("values", [])))

    def fetch_latest(self, symbol: str) -> Optional[Dict]:
        params = {
            "symbol": symbol,
            "interval": settings.INTERVAL,
            "outputsize": 1,
            "apikey": self.api_key,
        }
        r = requests.get(self.BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        values = data.get("values", [])
        return values[0] if values else None
