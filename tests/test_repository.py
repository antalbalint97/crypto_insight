from services.api.app.repositories import PriceReadRepository

def test_last_n(in_memory_db, sample_data):
    repo = PriceReadRepository()
    with in_memory_db as s:
        s.add_all(sample_data)
        s.commit()
        rows = repo.last_n(s, "AAPL", 2)
    assert len(rows) == 2
    assert rows[0].symbol == "AAPL"

def test_latest(in_memory_db, sample_data):
    repo = PriceReadRepository()
    with in_memory_db as s:
        s.add_all(sample_data)
        s.commit()
        latest = repo.latest(s, "AAPL")
    assert latest.close == 107
