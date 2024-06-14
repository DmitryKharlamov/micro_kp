# report_service/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    role = Column(String)
