from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.database import Base

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def create_test_database():
    Base.metadata.create_all(bind=engine)


def drop_test_database():
    Base.metadata.drop_all(bind=engine)