import pytest
from backend.app.db.session import Base, engine
from backend.app.db.seed import seed_database

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield
