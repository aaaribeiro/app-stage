import os
import requests
from app.database.crud.crudAppointment import CrudTimeAppointment
from app.domain.appointment import TimeAppointment
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

TOKEN = os.environ['TOKEN']
TAGS = ["listener",]
router = APIRouter()

@router.post(
    "/listener_ticket",
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


# @router.post(
#     "/listener_appointment",
#     tags=TAGS,
#     status_code=status.HTTP_200_OK, 
#     # dependencies=[Depends(auth.api_token)],
# )
# async def listener_appointment(request: Request, db: Session=Depends(get_db)):
#     try:
#         body = await request.json()
#         ticketId = body['Id']
#     except JSONDecodeError:
#         raise HTTPException(status_code=400, detail='incorrect format')

    # response = requests.get(f'https://api.movidesk.com/public/v1/tickets?token=27d95ace-819c-43d8-bb93-5c39dbf5edbd&id=5056&$select=id,subject,createdDate,ownerTeam&$filter=id%20eq%20{ticketId}&$expand=clients($select=id,businessName),clients($expand=organization($select=id,businessName)),owner,actions($select=origin,id),actions($expand=timeAppointments($expand=createdBy))')
    # print(response.url)
    # response.raise_for_status()
    # movidesk = response.json()
    # actions = movidesk.get('actions', '')
    # org = movidesk.get('clients', '')
    # agent = movidesk.get('owner', '')
    # agentTeam = movidesk.get('ownerTeam', '')

    # if not CrudTicket.readTicketById(db, ticketId):
    #     requests.post('http://localhost:8000/stage/movidesk/v1/listener_ticket',
    #         params={'Id': ticketId})
        
    # if org != '':
    #     orgId = org[0]['organization']['id'].upper()
    #     orgName = org[0]['organization']['businessName'].upper()
    #     if not CrudOrganization.readOrganizationById(db, orgId):
    #         payload = Organization(id=orgId, name=orgName)
    #         CrudOrganization.createOrganization(db, payload)
    
    # if agent != '':
    #     agentId = agent['id'].upper()
    #     agentName = agent['businessName'].upper()
    #     if not CrudAgent.readAgentById(db, agentId):
    #         payload = Agent(id=agentId, name=agentName, team=agentTeam)
    #         CrudAgent.createAgent(db, payload)

    # if actions != '' and len(actions) != 0:
    #     for action in actions:
    #         if len(action['timeAppointments']) != 0:
    #             for appointment in action['timeAppointments']:
    #                 if appointment['createdBy']['profileType'] in (2, 3):
    #                     appointedById = appointment['createdBy']['id']
    #                     appointedByName = appointment['createdBy']['businessName']
    #                     if not CrudAgent.readAgentById(db, appointedById):
    #                         payload = Agent(id=appointedById, name=appointedByName, team=agentTeam)
    #                         CrudAgent.createAgent(db, payload)
    #                     appointmentId = appointment['id']
    #                     workedTime = appointment['workTime']
    #                     createdDate = appointment['date']
    #                     if not CrudTimeAppointment.readTimeAppointmentById(db, appointmentId):
    #                         payload = TimeAppointment(id=appointmentId, agent_id=appointedById,
    #                             ticket_id=ticketId, time_appointment=workedTime, created_date=createdDate)
    #                         CrudTimeAppointment.createTimeAppointment(db, payload)
