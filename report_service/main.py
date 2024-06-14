# report_service/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import asyncio
import aio_pika
from . import models, schemas, database, report_generator

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/report", response_model=schemas.Report)
async def create_report(role: str, db: Session = Depends(get_db)):
    loop = asyncio.get_event_loop()
    report_content = await loop.run_in_executor(None, report_generator.generate_report, role)
    report = models.Report(content=report_content, role=role)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@app.get("/reports/{report_id}", response_model=schemas.Report)
def read_report(report_id: int, db: Session = Depends(get_db)):
    return db.query(models.Report).filter(models.Report.id == report_id).first()
