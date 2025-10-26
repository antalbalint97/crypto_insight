from pydantic import BaseSettings, Field
from typing import List

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    TWELVEDATA_API_KEY: str
    SYMBOLS: str
    INTERVAL: str = "1h"
    OUTPUTSIZE: int = 5000
    COLLECT_INTERVAL_SECONDS: int = 600

    class Config:
        env_file = ".env"

    @property
    def symbols_list(self) -> List[str]:
        return [s.strip() for s in self.SYMBOLS.split(",") if s.strip()]

settings = Settings()
