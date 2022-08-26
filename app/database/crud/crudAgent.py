from typing import List
from sqlalchemy.orm import Session
from app.database.models import Agents as ModelAgent
from app.domain.agent import Agent as DomainAgent


class CrudAgent:

    @classmethod
    def readAgents(self, db: Session, skip: int=0,
                    limit: int=100) -> List[ModelAgent]:
        return db.query(ModelAgent).\
            offset(skip).limit(limit).all()


    @classmethod
    def readAgentById(self, db: Session, id: str) -> ModelAgent:
        return db.query(ModelAgent).get(id)


    @classmethod
    def createAgent(self, db: Session, payload: DomainAgent) -> None:
        dbAgent = ModelAgent()
        for attr in payload.fields_set():
            setattr(dbAgent, attr, getattr(payload, attr))
        db.add(dbAgent)
        db.commit()


    @classmethod
    def updateAgent(self, db: Session, payload: DomainAgent,
                    id: str) -> None:
        dbAgent = self.readAgentById(db, id)
        for attr in payload.fields_set():
            setattr(dbAgent, attr, getattr(payload, attr))
        db.commit()


    @classmethod
    def deleteAgent(self, db: Session, id: str) -> None:
        dbAgent = self.readAgentById(db, id)
        db.delete(dbAgent)
        db.commit()
