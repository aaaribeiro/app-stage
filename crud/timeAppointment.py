from typing import List
from sqlalchemy.orm import Session

from database.models import TimeAppointments as Model
from domain.timeAppointment import TimeAppointment as Domain


class TimeAppointment:

    @classmethod
    def readTimeAppointments(self, db: Session, skip: int=0,
                            limit: int=100) -> List[Model]:
        return db.query(Model).offset(skip).\
            limit(limit).all()


    @classmethod
    def readTimeAppointmentById(self, db: Session, id: int) -> Model:
        return db.query(Model).get(id)
       

    @classmethod
    def createTimeAppointment(self, db: Session, payload: Domain) -> None:        
        dbTicket = Model()
        for attr in payload.fields_set():
            setattr(dbTicket, attr, getattr(payload, attr))
        db.add(dbTicket)
        db.commit()


    @classmethod
    def updateTimeAppointment(self, db: Session, payload: Domain,
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