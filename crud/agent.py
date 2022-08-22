from sqlalchemy.orm import Session

from database.models import Agents as ModelAgent
from domain.agent import Agent as DomainAgent


class Agent:

    def readAgents(self, db: Session, skip: int=0, limit: int=100):
        return db.query(ModelAgent).\
            offset(skip).limit(limit).all()


    def readAgentById(self, db: Session, id: str):
        return db.query(ModelAgent).get(id)


    def createAgent(self, db: Session, payload: DomainAgent):
        dbAgent = ModelAgent(
            id = payload.id,
            name = payload.name,
            team = payload.team,
        )
        db.add(dbAgent)
        db.commit()


    def updateAgent(self, db: Session, payload: DomainAgent,
                    dbAgent: ModelAgent):
        dbAgent.name = payload.name
        dbAgent.team = payload.team
        db.commit()


    def deleteAgent(self, db: Session, id: int):
        dbAgent = self.readAgentById(db, id)
        db.delete(dbAgent)
        db.commit()
