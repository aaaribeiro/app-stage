from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from domain.organization import Organization
from domain.agent import Agent


class TicketCreation(BaseModel):

    """
    Class used as reference to create new tickets.
    Tickets can't be created without id, organization and created_date.
    """

    id: int
    organization: Organization
    agent: Optional[Agent]
    created_date: datetime
    status: Optional[str]
    category: Optional[str]
    urgency: Optional[str]
    subject: Optional[str]
    sla_solution_date: Optional[datetime]
    sla_first_response: Optional[datetime]

    class Config:
        orm_mode = True


class TicketUpdate(BaseModel):

    """
    Class used as reference to update existing tickets.
    All fields are optional.
    """

    id: Optional[int]
    organization: Optional[Organization]
    agent: Optional[Agent]
    created_date: datetime
    status: Optional[str]
    category: Optional[str]
    urgency: Optional[str]
    subject: Optional[str]
    sla_solution_date: Optional[datetime]
    sla_first_response: Optional[datetime]

    class Config:
        orm_mode = True