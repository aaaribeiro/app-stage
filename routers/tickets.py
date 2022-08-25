from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from crud.ticket import Ticket as CRUD
from domain.ticket import TicketCreation as DomainCreation
from domain.ticket import TicketUpdate as DomainUpdate

from crud.organization import Organization as CRUDOrg
from crud.agent import Agent as CRUDAgent

from database.handlers import get_db

# authentication
# from auth import auth

# constants
TAGS = ["tickets",]

router = APIRouter()

@router.get(
    "/tickets",
    tags=TAGS,
    response_model=List[DomainCreation],
    # dependencies=[Depends(auth.api_token)],
)
async def read_tickets(skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    return CRUD.readTickets(db, skip, limit)


@router.get(
    "/tickets/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    response_model=DomainCreation,
    # dependencies=[Depends(auth.api_token)]
)
async def read_ticket(id: str, db:Session=Depends(get_db)):
    if not CRUD.readTicketById(db, id):
        raise HTTPException(status_code=404, detail="ticket not found")
    return CRUD.readTicketById(db, id)


@router.post(
    "/tickets",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)],
)
async def create_ticket(payload: DomainCreation,
                            db: Session=Depends(get_db)):
    if CRUD.readTicketById(db, payload.id):
        raise HTTPException(status_code=400, detail="ticket already exits")
    CRUD.createTicket(db, payload)



@router.patch(
    "/tickets/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def update_ticket(id: str, payload: DomainUpdate, 
                        db: Session = Depends(get_db)):
    if not CRUD.readTicketById(db, id):
        raise HTTPException(status_code=404, detail="ticket not found")

    if 'org_id' in [k for k, v in payload.dict().items() if v is not None]:
        if not CRUDOrg.readOrganizationById(db, payload.org_id):
            raise HTTPException(status_code=404, detail="organization not found")
    elif 'agent_id' in [k for k, v in payload.dict().items() if v is not None]:
        if not CRUDAgent.readAgentById(db, payload.agent_id):
            raise HTTPException(status_code=404, detail="agent not found")

    CRUD.updateTicket(db, payload, id) 



@router.delete(
    "/tickets/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_ticket(id: str, db: Session = Depends(get_db)):
    if not CRUD.readTicketById(db, id):
        raise HTTPException(status_code=404, detail="ticket not found")
    CRUD.deleteTicket(db, id)
