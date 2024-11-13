import logging
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import sys
import os
from models.parking import Base  # Base는 SQLAlchemy에서 테이블 정의를 위한 베이스 클래스입니다.

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 환경 변수 설정 (secret.yaml에 맞춰 설정)
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_HOST')
DB_NAME = os.getenv('MYSQL_DATABASE')
DB_PORT = os.getenv('MYSQL_PORT')

logging.info(f"DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}, DB_HOST: {DB_HOST}, DB_NAME: {DB_NAME}, DB_PORT: {DB_PORT}")

db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = sqlalchemy.create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    try:
        Base.metadata.create_all(engine)  # Base 클래스에서 정의된 모든 테이블을 생성
        logging.info("Tables created successfully.")
    except Exception as e:
        logging.error("Error creating tables: %s", e)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # 세션을 안전하게 닫아 자원을 해제합니다.
