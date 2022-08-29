import requests
from typing import List
from fastapi import Depends, APIRouter, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database.crud.crudTicket import CrudTicket
from app.database.crud.crudOrganization import CrudOrganization
from app.database.crud.crudAgent import CrudAgent
from app.domain.ticket import Ticket
from app.domain.organization import Organization
from app.domain.agent import Agent

from app.database.dbHandlers import get_db
from json import JSONDecodeError
# from auth import auth


# constants
TAGS = ["listener",]
router = APIRouter()

# @router.get(
#     "/tickets",
#     tags=TAGS,
#     response_model=List[Ticket],
#     # dependencies=[Depends(auth.api_token)],
# )
# async def read_tickets(skip: int = 0, limit: int = 100,
#                             db: Session = Depends(get_db)):
#     return CrudTicket.readTickets(db, skip, limit)


# @router.get(
#     "/tickets/{id}",
#     tags=TAGS,
#     status_code=status.HTTP_200_OK,
#     response_model=Ticket,
#     # dependencies=[Depends(auth.api_token)]
# )
# async def read_ticket(id: str, db:Session=Depends(get_db)):
#     if not CrudTicket.readTicketById(db, id):
#         raise HTTPException(status_code=404, detail="ticket not found")
#     return CrudTicket.readTicketById(db, id)


@router.post(
    "/listener",
    tags=TAGS,
    status_code=status.HTTP_200_OK, 
    # dependencies=[Depends(auth.api_token)],
)
async def listener_ticket(request: Request, db: Session=Depends(get_db)):
    try:
        body = await request.json()
        ticketId = body['Id']
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail='format incorrect')

    params = {'token': '27d95ace-819c-43d8-bb93-5c39dbf5edbd', 'id': ticketId} # TO-DO -> improve security
    response = requests.get('https://api.movidesk.com/public/v1/tickets', params=params)
    
    movidesk = response.json()
    org = movidesk.get('clients', '')
    agent = movidesk.get('owner', '')
    agentTeam = movidesk.get('ownerTeam', '')
    ticketSubject = movidesk.get('subject', '')
    ticketCategory = movidesk.get('category', '')
    ticketUrgency = movidesk.get('urgency', '')
    ticketStatus = movidesk.get('status', '')
    ticketCreatedDate = movidesk.get('createdDate', '')
    ticketSlaSolutionDate = movidesk.get('slaSolutionDate', '')
    ticketSlaResponseDate = movidesk.get('slaResponseDate', '')
    
    if org != '':
        orgId = org[0]['organization']['id']
        orgName = org[0]['organization']['businessName']
        if not CrudOrganization.readOrganizationById(db, orgId):
            payload = Organization(id=orgId, name=orgName)
            CrudOrganization.createOrganization(db, payload)

    if agent != '':
        agentId = agent['id']
        agentName = agent['businessName']
        if not CrudAgent.readAgentById(db, agentId):
            payload = Agent(id=agentId, name=agentName, team=agentTeam)
            CrudAgent.createAgent(db, payload)
        
    if not CrudTicket.readTicketById(db, ticketId):
        payload = Ticket(id=ticketId, org_id=orgId, agent_id=agentId,
            created_date=ticketCreatedDate, status=ticketStatus,
            category=ticketCategory, urgency=ticketUrgency,
            subject=ticketSubject, sla_first_response=ticketSlaResponseDate,
            sla_solution_date=ticketSlaSolutionDate)
        CrudTicket.createTicket(db, payload)
    
    
    # org, agent = movidesk['clients'][0], movidesk['owner']
    # org_id = movidesk['clients'][0]['organization']['id']
    # org_name = movidesk

    # if CrudTicket.readTicketById(db, payload.id):
    #     raise HTTPException(status_code=400, detail="ticket already exits")
    # CrudTicket.createTicket(db, payload)


# @router.patch(
#     "/tickets/{id}",
#     tags=TAGS,
#     status_code=status.HTTP_200_OK,
#     # dependencies=[Depends(auth.api_token)],
# )
# async def update_ticket(id: str, payload: Ticket, 
#                         db: Session = Depends(get_db)):
#     if not CrudTicket.readTicketById(db, id):
#         raise HTTPException(status_code=404, detail="ticket not found")

#     if 'org_id' in [k for k, v in payload.dict().items() if v is not None]:
#         if not CrudOrganization.readOrganizationById(db, payload.org_id):
#             raise HTTPException(status_code=404, detail="organization not found")
            
#     elif 'agent_id' in [k for k, v in payload.dict().items() if v is not None]:
#         if not CrudAgent.readAgentById(db, payload.agent_id):
#             raise HTTPException(status_code=404, detail="agent not found")

#     CrudTicket.updateTicket(db, payload, id) 



# @router.delete(
#     "/tickets/{id}",
#     tags=TAGS,
#     status_code=status.HTTP_200_OK,
#     # dependencies=[Depends(auth.api_token)],
# )
# async def delete_ticket(id: str, db: Session = Depends(get_db)):
#     if not CrudTicket.readTicketById(db, id):
#         raise HTTPException(status_code=404, detail="ticket not found")
#     CrudTicket.deleteTicket(db, id)
