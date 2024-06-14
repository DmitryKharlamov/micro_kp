from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Создаем экземпляр класса Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем экземпляр класса SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей
Base = declarative_base()

# Функция для подключения к базе данных
def connect():
    return engine.connect()

# Функция для отключения от базы данных
def disconnect(connection):
    connection.close()
