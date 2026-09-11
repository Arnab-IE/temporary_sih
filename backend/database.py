import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# 1. Clean unsupported Neon query parameters if present
if "channel_binding=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("&channel_binding=")[0].split("?channel_binding=")[0]

# 2. Convert protocol scheme to explicit psycopg2 driver format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# 3. Initialize SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency to yield a clean database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
