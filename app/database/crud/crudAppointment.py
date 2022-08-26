from typing import List
from sqlalchemy.orm import Session
from app.database.models import TimeAppointments as ModelAppointment
from app.domain.appointment import TimeAppointment as DomainAppointment


class CrudTimeAppointment:

    @classmethod
    def readTimeAppointments(self, db: Session, skip: int=0,
                            limit: int=100) -> List[ModelAppointment]:
        return db.query(ModelAppointment).offset(skip).\
            limit(limit).all()


    @classmethod
    def readTimeAppointmentById(self, db: Session, id: int) -> ModelAppointment:
        return db.query(ModelAppointment).get(id)
       

    @classmethod
    def createTimeAppointment(self, db: Session, payload: DomainAppointment) -> None:        
        dbTicket = ModelAppointment()
        for attr in payload.fields_set():
            setattr(dbTicket, attr, getattr(payload, attr))
        db.add(dbTicket)
        db.commit()


    @classmethod
    def updateTimeAppointment(self, db: Session, payload: DomainAppointment,
                            id: str) -> None:
        dbTicket = self.readTimeAppointmentById(db, id)
        for attr in payload.fields_set():
            setattr(dbTicket, attr, getattr(payload, attr))
        db.commit()


    @classmethod
    def deleteTimeAppointment(self, db: Session, id: str) -> None:
        dbTicket = self.readTimeAppointmentById(db, id)
        db.delete(dbTicket)
        db.commit()