import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine() -> Engine:
    database_url = os.environ["DATABASE_URL"]
    return create_engine(database_url)


def get_session_local() -> sessionmaker:
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)
