from sqlmodel import SQLModel, create_engine
from app.config import settings

engine = create_engine(settings.postgres_uri)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)