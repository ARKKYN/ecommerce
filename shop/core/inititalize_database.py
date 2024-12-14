from sqlmodel import SQLModel, create_engine, Session
from shop.config.database import FILE_PATH

engine = None

def get_engine():
    global engine
    if engine is None:
        initialize_database()
    return engine

def get_session():
    global engine
    if engine is None:
        initialize_database()
    return Session(engine)

def initialize_database():
    global engine
    sqlite_url = f"sqlite:///{FILE_PATH}"
    engine = create_engine(sqlite_url, echo=False, pool_size=200000, max_overflow=300000, pool_timeout=60, pool_pre_ping=True)
    SQLModel.metadata.create_all(engine)
    return engine
