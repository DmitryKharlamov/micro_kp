import sys
from pathlib import Path
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import asyncio
import aio_pika

# Добавляем путь к корневой директории проекта в sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from report_service import models, schemas, database, report_generator

app = FastAPI()

# Подключение к базе данных при старте приложения
@app.on_event("startup")
def startup_event():
    database.connect()

# Отключение от базы данных при остановке приложения
@app.on_event("shutdown")
def shutdown_event():
    database.disconnect()

# Функция для получения экземпляра сессии базы данных
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание отчёта
@app.post("/report", response_model=schemas.Report)
async def create_report(role: str, db: Session = Depends(get_db)):
    loop = asyncio.get_event_loop()
    report_content = await loop.run_in_executor(None, report_generator.generate_report, role)
    report = models.Report(content=report_content, role=role)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
