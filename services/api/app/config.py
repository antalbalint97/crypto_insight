import os
from typing import List, ClassVar
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Database ---
    POSTGRES_HOST: str = Field("localhost")
    POSTGRES_PORT: int = Field(5432)
    POSTGRES_DB: str = Field("crypto_insight")
    POSTGRES_USER: str = Field("postgres")
    POSTGRES_PASSWORD: str = Field("postgres")

    # --- API Configuration ---
    TWELVEDATA_API_KEY: str = Field("dummy_api_key")
    SYMBOLS: str = Field("AAPL,MSFT,BTC-USD")
    INTERVAL: str = Field("1h")
    OUTPUTSIZE: int = Field(5000)
    COLLECT_INTERVAL_SECONDS: int = Field(600)

    # --- Environment loading ---
    env_file: ClassVar[str] = ".env" if os.path.exists(".env") else ".env.dev"
    model_config = SettingsConfigDict(env_file=env_file, extra="ignore")

    @property
    def symbols_list(self) -> List[str]:
        """Return SYMBOLS as a clean list."""
        return [s.strip() for s in self.SYMBOLS.split(",") if s.strip()]


settings = Settings()
