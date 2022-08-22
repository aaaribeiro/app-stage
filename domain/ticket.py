from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .organization import Organization
from .agent import Agent


class Ticket(BaseModel):
    id: Optional[int]
    organization: Organization
    agent: Agent
    created_date: datetime
    status: Optional[str]
    category: Optional[str]
    urgency: Optional[str]
    subject: Optional[str]
    sla_solution_date: Optional[datetime]
    sla_first_response: Optional[datetime]

    class Config:
        orm_mode = True