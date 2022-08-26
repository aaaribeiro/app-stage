from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database.crud.crudAgent import CrudAgent
from app.domain.agent import Agent
from app.database.dbHandlers import get_db
# from auth import auth


TAGS = ['agents',]

router = APIRouter()

@router.get(
    "/agents",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    response_model=List[Agent],
    # dependencies=[Depends(auth.api_token)]
)
async def read_agents(skip: int = 0, limit: int = 100,
                    db:Session=Depends(get_db)):
    return CrudAgent.readAgents(db, skip, limit)


@router.get(
    "/agents/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    response_model=Agent,
    # dependencies=[Depends(auth.api_token)]
)
async def read_agent(id: str, db:Session=Depends(get_db)):
    if not CrudAgent.readAgentById(db, id):
        raise HTTPException(status_code=404, detail="agent not found")
    return CrudAgent.readAgentById(db, id)


@router.post(
    "/agents",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)]
)
async def create_agent(payload: Agent, db: Session=Depends(get_db)):   
    if CrudAgent.readAgentById(db, payload.id):
        raise HTTPException(status_code=400, detail="agent already exists")
    CrudAgent.createAgent(db, payload)


@router.patch(
    "/agents/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def update_agent(id: str, payload: Agent, 
                        db: Session = Depends(get_db)):
    if not CrudAgent.readAgentById(db, id):
        raise HTTPException(status_code=404, detail="agent not found")
    CrudAgent.updateAgent(db, payload, id)
    

@router.delete(
    "/agents/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_agent(id: str, db: Session = Depends(get_db)):
    if not CrudAgent.readAgentById(db, id):
        raise HTTPException(status_code=404, detail="agent not found")
    CrudAgent.deleteAgent(db, id)
    