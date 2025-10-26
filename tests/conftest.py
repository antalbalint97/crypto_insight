import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.api.app.models import Base, StockPrice
from datetime import datetime


@pytest.fixture(scope="function")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    yield Session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_data():
    return [
        StockPrice(
            symbol="AAPL",
            datetime=datetime(2024, 1, 1, 10),
            open=100,
            high=105,
            low=99,
            close=104,
            volume=1200,
        ),
        StockPrice(
            symbol="AAPL",
            datetime=datetime(2024, 1, 1, 11),
            open=104,
            high=107,
            low=103,
            close=106,
            volume=1000,
        ),
        StockPrice(
            symbol="AAPL",
            datetime=datetime(2024, 1, 1, 12),
            open=106,
            high=108,
            low=105,
            close=107,
            volume=900,
        ),
    ]
