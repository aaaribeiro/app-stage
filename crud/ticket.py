from typing import List
from sqlalchemy.orm import Session

from database.models import Tickets as ModelTicket
from domain.ticket import TicketCreation as DomainTicketCreation
from domain.ticket import TicketUpdate as DomainTicketUpdate


class Ticket:

    @classmethod
    def readTickets(self, db: Session, skip: int=0,
                            limit: int=100) -> List[ModelTicket]:
        return db.query(ModelTicket).offset(skip).\
            limit(limit).all()


    @classmethod
    def readTicketById(self, db: Session, id: str) -> ModelTicket:
        return db.query(ModelTicket).get(id)


    @classmethod
    def readTicketById(self, db: Session, id: str) -> ModelTicket:
        return db.query(ModelTicket).get(id)
       

    @classmethod
    def createTicket(self, db: Session, payload: DomainTicketCreation) -> None:
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
        """
        
        dbTicket = ModelTicket(
            id = payload.id,
            organization = payload.organization,
            created_date = payload.created_date,
            status = payload.status,
            category = payload.category,
            urgency = payload.category,
            subject = payload.subject,
            sla_solution_date = payload.sla_solution_date,
            sla_first_response = payload.sla_first_response
            )
        db.add(dbTicket)
        db.commit()


    @classmethod
    def updateTicket(self, db: Session, payload: DomainTicketUpdate,
                            id: str) -> None:
        dbTicket = self.readTicketById(db, id)
        if payload.name is not None:
            dbTicket.name = payload.name
        db.commit()


    @classmethod
    def deleteTicket(self, db: Session, id: str) -> None:
        dbTicket = self.readTicketById(db, id)
        db.delete(dbTicket)
        db.commit()