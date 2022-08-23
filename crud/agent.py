from typing import List
from sqlalchemy.orm import Session

from database.models import Agents as ModelAgent
from domain.agent import Agent as DomainAgent


class Agent:

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
        dbAgent = ModelAgent(
            id = payload.id,
            name = payload.name,
            team = payload.team,
        )
        db.add(dbAgent)
        db.commit()


    @classmethod
    def updateAgent(self, db: Session, payload: DomainAgent,
                    id: str) -> None:
        dbAgent = self.readAgentById(db, id)
        if payload.name is not None:
            dbAgent.name = payload.name
        if payload.team is not None:
            dbAgent.team = payload.team
        db.commit()


    # @classmethod
    # def updateAgent(self, db: Session, payload: DomainAgent,
    #                 dbAgent: ModelAgent) -> None:
    #     dbAgent.name = payload.name
    #     dbAgent.team = payload.team
    #     db.commit()


    @classmethod
    def deleteAgent(self, db: Session, id: str) -> None:
        dbAgent = self.readAgentById(db, id)
        db.delete(dbAgent)
        db.commit()
