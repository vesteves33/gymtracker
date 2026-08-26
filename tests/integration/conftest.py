import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg2://gymtracker:gymtracker@localhost:5432/gymtracker",
)
os.environ.setdefault("JWT_SECRET", "test-secret")

import pytest
from sqlalchemy.orm import Session

from app.infrastructure.db.session import Base, get_engine


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    engine = get_engine()
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session():
    engine = get_engine()
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
