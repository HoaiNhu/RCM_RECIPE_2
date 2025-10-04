# scripts/init_db.py
from sqlalchemy import create_engine
from infrastructure.db.models import Base
from configs.settings import settings

def init_database():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()