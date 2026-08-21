from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path


# หาโฟลเดอร์ project หลัก
BASE_DIR = Path(__file__).resolve().parent.parent

# สร้างโฟลเดอร์ data ถ้ายังไม่มี
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# SQLite database
DATABASE_URL = f"sqlite:///{DATA_DIR / 'wastewater.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()