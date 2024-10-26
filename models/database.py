import os
from dotenv import load_dotenv
from typing import Generator, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(os.path.join(os.getcwd(), 'venv/.env'))

#El comentado es para agarrar el backend del Docker
DATABASE_URL = os.getenv('DATABASE_URL')

#DATABASE_URL = 'mysql+mysqlconnector://root:root@localhost:3306/ecommerce'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Any, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()