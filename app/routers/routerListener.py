import os
import requests
# from typing import List
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

try: TOKEN = os.environ['TOKEN']
except KeyError: TOKEN = '27d95ace-819c-43d8-bb93-5c39dbf5edbd'
TAGS = ["listener",]
router = APIRouter()

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
        raise HTTPException(status_code=400, detail='incorrect format')

    params = {'token': TOKEN, 'id': ticketId}
    response = requests.get('https://api.movidesk.com/public/v1/tickets', params=params)
    
    movidesk = response.json()
    org = movidesk.get('clients', '')
    agent = movidesk.get('owner', '')
    agentTeam = movidesk.get('ownerTeam', '').upper()
    ticketSubject = movidesk.get('subject', '').upper()
    ticketCategory = movidesk.get('category', '').upper()
    ticketUrgency = movidesk.get('urgency', '').upper()
    ticketStatus = movidesk.get('status', '').upper()
    ticketCreatedDate = movidesk.get('createdDate', '')
    ticketSlaSolutionDate = movidesk.get('slaSolutionDate', '')
    ticketSlaResponseDate = movidesk.get('slaResponseDate', '')
    
    if org != '':
        orgId = org[0]['organization']['id'].upper()
        orgName = org[0]['organization']['businessName'].upper()
        if not CrudOrganization.readOrganizationById(db, orgId):
            payload = Organization(id=orgId, name=orgName)
            CrudOrganization.createOrganization(db, payload)

    if agent != '':
        agentId = agent['id'].upper()
        agentName = agent['businessName'].upper()
        if not CrudAgent.readAgentById(db, agentId):
            payload = Agent(id=agentId, name=agentName, team=agentTeam)
            CrudAgent.createAgent(db, payload)
        
    payload = Ticket(id=ticketId, org_id=orgId, agent_id=agentId,
        created_date=ticketCreatedDate, status=ticketStatus,
        category=ticketCategory, urgency=ticketUrgency,
        subject=ticketSubject, sla_first_response=ticketSlaResponseDate,
        sla_solution_date=ticketSlaSolutionDate)
    
    if not CrudTicket.readTicketById(db, ticketId):
        CrudTicket.createTicket(db, payload)
    else:
        CrudTicket.updateTicket(db, payload, ticketId)