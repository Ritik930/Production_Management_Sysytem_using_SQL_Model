
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql://postgres:Cybershot903@localhost:5432/prac_db"

# Remove the SQLite-specific connect_args for PostgreSQL
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session