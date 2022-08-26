from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database.crud.crudTicket import CrudTicket
from app.domain.ticket import Ticket
from app.database.crud.crudOrganization import CrudOrganization
from app.database.crud.crudAgent import CrudAgent
from app.database.dbHandlers import get_db
# from auth import auth


# constants
TAGS = ["tickets",]
router = APIRouter()

@router.get(
    "/tickets",
    tags=TAGS,
    response_model=List[Ticket],
    # dependencies=[Depends(auth.api_token)],
)
async def read_tickets(skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    return CrudTicket.readTickets(db, skip, limit)


@router.get(
    "/tickets/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    response_model=Ticket,
    # dependencies=[Depends(auth.api_token)]
)
async def read_ticket(id: str, db:Session=Depends(get_db)):
    if not CrudTicket.readTicketById(db, id):
        raise HTTPException(status_code=404, detail="ticket not found")
    return CrudTicket.readTicketById(db, id)


@router.post(
    "/tickets",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)],
)
async def create_ticket(payload: Ticket,
                            db: Session=Depends(get_db)):
    if CrudTicket.readTicketById(db, payload.id):
        raise HTTPException(status_code=400, detail="ticket already exits")
    CrudTicket.createTicket(db, payload)



@router.patch(
    "/tickets/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def update_ticket(id: str, payload: Ticket, 
                        db: Session = Depends(get_db)):
    if not CrudTicket.readTicketById(db, id):
        raise HTTPException(status_code=404, detail="ticket not found")

    if 'org_id' in [k for k, v in payload.dict().items() if v is not None]:
        if not CrudOrganization.readOrganizationById(db, payload.org_id):
            raise HTTPException(status_code=404, detail="organization not found")
            
    elif 'agent_id' in [k for k, v in payload.dict().items() if v is not None]:
        if not CrudAgent.readAgentById(db, payload.agent_id):
            raise HTTPException(status_code=404, detail="agent not found")

    CrudTicket.updateTicket(db, payload, id) 



@router.delete(
    "/tickets/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_ticket(id: str, db: Session = Depends(get_db)):
    if not CrudTicket.readTicketById(db, id):
        raise HTTPException(status_code=404, detail="ticket not found")
    CrudTicket.deleteTicket(db, id)
