# report_service/report_generator.py
import time
from fastapi import HTTPException

def generate_report(role: str):
    if role == "ace":
        time.sleep(20)
    elif role == "king":
        time.sleep(15)
    elif role in ["queen", "jack"]:
        time.sleep(10)
    else:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Симуляция данных отчета
    data = {
        "ace": "Полный отчет",
        "king": "Отчет по регионам",
        "queen": "Отчет по городам",
        "jack": "Отчет по магазинам"
    }
    return data.get(role, "Нет данных")
