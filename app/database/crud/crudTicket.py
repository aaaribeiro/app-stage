from typing import List
from sqlalchemy.orm import Session
from app.database.models import Tickets as ModelTicket
from app.domain.ticket import Ticket as DomainTicket


class CrudTicket:

    @classmethod
    def readTickets(self, db: Session, skip: int=0,
                            limit: int=100) -> List[ModelTicket]:
        return db.query(ModelTicket).offset(skip).\
            limit(limit).all()


    @classmethod
    def readTicketById(self, db: Session, id: int) -> ModelTicket:
        return db.query(ModelTicket).get(id)
       

    @classmethod
    def createTicket(self, db: Session, payload: DomainTicket) -> None:        
        dbTicket = ModelTicket()
        for attr in payload.fields_set():
            setattr(dbTicket, attr, getattr(payload, attr))
        db.add(dbTicket)
        db.commit()


    @classmethod
    def updateTicket(self, db: Session, payload: DomainTicket,
                            id: int) -> None:
        dbTicket = self.readTicketById(db, id)
        for attr in payload.fields_set():
            setattr(dbTicket, attr, getattr(payload, attr))
        db.commit()


    @classmethod
    def deleteTicket(self, db: Session, id: int) -> None:
        dbTicket = self.readTicketById(db, id)
        db.delete(dbTicket)
        db.commit()