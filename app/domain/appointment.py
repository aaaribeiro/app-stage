from datetime import datetime, time
from typing import Optional
from app.domain.base import Base
# from domain.timeAppointment import TimeAppointment
# from domain.timeAppointment import


class TimeAppointment(Base):
    id: Optional[int]
    ticket_id: Optional[int]
    agent_id: Optional[str]
    time_appointment: Optional[time]
    created_date: Optional[datetime]

    class Config:
        orm_mode = True