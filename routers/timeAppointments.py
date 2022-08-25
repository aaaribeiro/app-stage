from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from crud.timeAppointment import TimeAppointment as CRUD
from domain.timeAppointment import TimeAppointment as Domain

from crud.ticket import Ticket as CRUDTicket
from crud.agent import Agent as CRUDAgent

from database.handlers import get_db

# authentication
# from auth import auth

# constants
TAGS = ["appointments",]

router = APIRouter()

@router.get(
    "/timeappointments",
    tags=TAGS,
    response_model=List[Domain],
    # dependencies=[Depends(auth.api_token)],
)
async def read_time_appointments(skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    return CRUD.readTickets(db, skip, limit)


@router.get(
    "/timeappointments/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    response_model=Domain,
    # dependencies=[Depends(auth.api_token)]
)
async def read_time_appointment(id: int, db:Session=Depends(get_db)):
    if not (dbTimeAppointment := CRUD.readTimeAppointmentById(db, id)):
        raise HTTPException(status_code=404, detail="time appointment not found")
    return dbTimeAppointment


@router.post(
    "/timeappointments",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)],
)
async def create_ticket(payload: Domain,
                            db: Session=Depends(get_db)):
    if CRUD.readTimeAppointmentById(db, payload.id):
        raise HTTPException(status_code=400, detail="time appointment already exits")
    CRUD.createTimeAppointment(db, payload)



@router.patch(
    "/timeappointments/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def update_ticket(id: int, payload: Domain, 
                        db: Session = Depends(get_db)):
    if not CRUD.readTimeAppointmentById(db, id):
        raise HTTPException(status_code=404, detail="time appointment not found")

    if 'ticket_id' in [k for k, v in payload.dict().items() if v is not None]:
        if not CRUDTicket.readTicketById(db, payload.ticket_id):
            raise HTTPException(status_code=404, detail="ticket not found")

    elif 'agent_id' in [k for k, v in payload.dict().items() if v is not None]:
        if not CRUDAgent.readAgentById(db, payload.agent_id):
            raise HTTPException(status_code=404, detail="agent not found")

    CRUD.updateTimeAppointment(db, payload, id) 



@router.delete(
    "/timeappointments/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_time_appointment(id: int, db: Session = Depends(get_db)):
    if not CRUD.readTimeAppointmentById(db, id):
        raise HTTPException(status_code=404, detail="time appointment not found")
    CRUD.deleteTimeAppointment(db, id)
