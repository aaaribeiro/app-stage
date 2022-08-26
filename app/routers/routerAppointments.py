from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database.crud.crudAppointment import CrudTimeAppointment
from app.database.crud.crudTicket import CrudTicket
from app.database.crud.crudAgent import CrudAgent
from app.domain.appointment import TimeAppointment
from app.database.dbHandlers import get_db
# from auth import auth

# constants
TAGS = ["appointments",]

router = APIRouter()

@router.get(
    "/timeappointments",
    tags=TAGS,
    response_model=List[TimeAppointment],
    # dependencies=[Depends(auth.api_token)],
)
async def read_time_appointments(skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    return CrudTimeAppointment.readTimeAppointments(db, skip, limit)


@router.get(
    "/timeappointments/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    response_model=TimeAppointment,
    # dependencies=[Depends(auth.api_token)]
)
async def read_time_appointment(id: int, db:Session=Depends(get_db)):
    if not (dbTimeAppointment := CrudTimeAppointment.readTimeAppointmentById(db, id)):
        raise HTTPException(status_code=404, detail="time appointment not found")
    return dbTimeAppointment


@router.post(
    "/timeappointments",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)],
)
async def create_ticket(payload: TimeAppointment,
                            db: Session=Depends(get_db)):
    if CrudTimeAppointment.readTimeAppointmentById(db, payload.id):
        raise HTTPException(status_code=400, detail="time appointment already exits")
    CrudTimeAppointment.createTimeAppointment(db, payload)



@router.patch(
    "/timeappointments/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def update_ticket(id: int, payload: TimeAppointment, 
                        db: Session = Depends(get_db)):
    if not CrudTimeAppointment.readTimeAppointmentById(db, id):
        raise HTTPException(status_code=404, detail="time appointment not found")

    if 'ticket_id' in [k for k, v in payload.dict().items() if v is not None]:
        if not CrudTicket.readTicketById(db, payload.ticket_id):
            raise HTTPException(status_code=404, detail="ticket not found")

    elif 'agent_id' in [k for k, v in payload.dict().items() if v is not None]:
        if not CrudAgent.readAgentById(db, payload.agent_id):
            raise HTTPException(status_code=404, detail="agent not found")

    CrudTimeAppointment.updateTimeAppointment(db, payload, id) 



@router.delete(
    "/timeappointments/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_time_appointment(id: int, db: Session = Depends(get_db)):
    if not CrudTimeAppointment.readTimeAppointmentById(db, id):
        raise HTTPException(status_code=404, detail="time appointment not found")
    CrudTimeAppointment.deleteTimeAppointment(db, id)
