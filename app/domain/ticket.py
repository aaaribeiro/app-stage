from datetime import datetime
from typing import Optional
from app.domain.base import Base


class Ticket(Base):

    """
    Class used as reference to update existing tickets and create new ones.
    All fields are optional.
    """

    id: Optional[int]
    org_id: Optional[str]
    agent_id: Optional[str]
    created_date: Optional[datetime]
    status: Optional[str]
    category: Optional[str]
    urgency: Optional[str]
    subject: Optional[str]
    sla_solution_date: Optional[datetime]
    sla_first_response: Optional[datetime]

    class Config:
        orm_mode = True