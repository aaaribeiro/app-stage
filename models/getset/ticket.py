from sqlalchemy.orm import Session
from models import models
from serializers import schemas


class Ticket:
    
    @classmethod
    def readTickets(self, db: Session, skip: int=0, limit: int=100):
        return db.query(models.Tickets).\
            order_by(models.Tickets.ticket_id).all()

    
    @classmethod
    def readTicketById(self, db: Session, id: int):
        return db.query(models.Tickets).get(id)
    

    @classmethod
    def createTicket(self, db: Session, payload: schemas.Ticket):
        ticket = models.Tickets(
            ticket_id = payload.ticket_id,
            organization_id = payload.organization_id,
            agent_id = payload.agent_id,
            status = payload.status,
            category = payload.category,
            urgency = payload.urgency,
            subject = payload.subject,
            created_date = payload.created_date,
            sla_solution_date = payload.sla_solution_date,
            sla_first_response = payload.sla_first_response,
        )
        db.add(ticket)               
        db.commit()


    @classmethod
    def updateTicket(self, db: Session, payload: schemas.Ticket,
                    dbTicket: models.Tickets):
        dbTicket.organization_id = payload.organization_id
        dbTicket.agent_id = payload.agent_id
        dbTicket.status = payload.status
        dbTicket.category = payload.category
        dbTicket.urgency = payload.urgency
        dbTicket.subject = payload.subject
        dbTicket.created_date = payload.created_date
        dbTicket.sla_first_response = payload.sla_first_response
        dbTicket.sla_solution_date = payload.sla_solution_date
        db.commit()


    @classmethod
    def deleteTicket(self, db: Session, id: int):
        dbTicket = self.readTicketById(db, id)
        db.delete(dbTicket)
        db.commit()
