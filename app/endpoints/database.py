from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:marcuscruz@localhost/fastapi_app"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Dependency
# Database Connection Management

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def connect_to_database():
    while True:
        try: 
            conn = psycopg2.connect(host="localhost", database="fastapi_app", user="postgres",
                                    password="marcuscruz", cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("Database connection was successful")
            return conn, cursor
        except Exception as error:
            print("Connection to database failed")
            print("Error: ", error)
            time.sleep(2)




