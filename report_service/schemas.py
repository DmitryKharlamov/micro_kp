# report_service/schemas.py
from pydantic import BaseModel

class ReportBase(BaseModel):
    content: str
    role: str

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int

    class Config:
        orm_mode = True
