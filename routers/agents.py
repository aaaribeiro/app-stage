from typing import List

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from crud.agent import Agent as CRUDAgent
from domain.agent import Agent as DomainAgent
# from auth import auth
from database.handlers import get_db

TAGS = ["agents",]

router = APIRouter()

@router.get(
    "/agents",
    tags=TAGS, status_code=status.HTTP_200_OK, response_model=List[DomainAgent],
    # dependencies=[Depends(auth.api_token)]
)
async def read_agents(skip: int = 0, limit: int = 100,
                    db:Session=Depends(get_db)):
    crud = CRUDAgent()
    return crud.readAgents(db, skip, limit)


@router.post(
    "/agents",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)]
)
async def create_agent(payload: DomainAgent, db: Session=Depends(get_db)):
    crud = CRUDAgent()    
    dbAgent = crud.readAgentById(db, payload.id)  
    if dbAgent:
        raise HTTPException(status_code=400, detail="agent already exists")
    crud.createAgent(db, payload)


@router.put(
    "/agents/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def update_agent(id: str, payload: DomainAgent, 
                        db: Session = Depends(get_db)):
    crud = CRUDAgent()
    dbAgent = crud.readAgentById(db, id)
    if not dbAgent:
        raise HTTPException(status_code=404, detail="agent not found")
    crud.updateAgent(db, payload, dbAgent)  
    

@router.delete(
    "/agents/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_agent(id: str, db: Session = Depends(get_db)):
    crud = CRUDAgent()
    dbAgent = crud.readAgentById(db, id)
    if not dbAgent:
        raise HTTPException(status_code=404, detail="agent not found")
    crud.deleteAgent(db, id)
    