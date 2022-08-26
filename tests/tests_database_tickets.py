import sys
import os.path
sys.path.insert(0, os.path.abspath('.'))

import unittest
from datetime import datetime
from app.database.dbHandlers import DbHandler
from app.database.models import Tickets
from app.domain.ticket import Ticket
from app.domain.organization import Organization
from app.domain.agent import Agent
from app.database.crud.crudTicket import CrudTicket
from app.database.crud.crudAgent import CrudAgent
from app.database.crud.crudOrganization import CrudOrganization


class TestTicketDB(unittest.TestCase):
    
    def setUp(self):
        self.domain_org = Organization(
            id = 'ORG001',
            name = 'ORG TEST'
        )

        self.domain_org_update = Organization(
            id = 'ORG002',
            name = 'ORG UP-TO-DATE'
        )

        self.domain_agent = Agent(
            id = 'AGT001',
            name = 'AGENT TEST',
            team = 'BSS'
        )

        self.domain_agent_update = Agent(
                id = 'AGT002',
                name = 'AGENT UP-TO-DATE',
                team = 'BSS'
        )

        self.domain_ticket = Ticket(
            id = 1,
            org_id = 'ORG001',
            agent_id = 'AGT001',
            created_date = datetime.now(),
            status = 'NEW',
            category = 'HELP REQUEST',
            urgency = 'B-HIGH',
            subject = 'TTCKET TEST' 
        )


    def test_a_add_ticket_db(self):
        with DbHandler() as db:
            self.assertIsNone(CrudOrganization.createOrganization(db, self.domain_org))
            self.assertIsNone(CrudOrganization.createOrganization(db, self.domain_org_update))
            self.assertIsNone(CrudAgent.createAgent(db, self.domain_agent))
            self.assertIsNone(CrudAgent.createAgent(db, self.domain_agent_update))
            self.assertIsNone(CrudTicket.createTicket(db, self.domain_ticket))
            
    
    def test_b_read_ticket_db(self):
        with DbHandler() as db:
            self.model_ticket = CrudTicket.readTicketById(db, self.domain_ticket.id)
            self.model_ticket_expected = CrudTicket()
            for attr in self.domain_ticket.fields_set():
                setattr(self.model_ticket_expected, attr, getattr(self.domain_ticket, attr))
            self.domain_expected = Ticket.from_orm(self.model_ticket_expected)
            self.assertIsInstance(self.model_ticket, Tickets)
            self.assertEqual(self.domain_expected, self.domain_ticket)


    def test_c_update_ticket_db(self):
        with DbHandler() as db:
            self.domain_ticket_update = Ticket(status = 'IN PROGRESS')
            self.assertIsNone(CrudTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CrudTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('IN PROGRESS', self.model_ticket_update.status)

            self.domain_ticket_update = Ticket(category = 'INCIDENT')
            self.assertIsNone(CrudTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CrudTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('INCIDENT', self.model_ticket_update.category)

            self.domain_ticket_update = Ticket(urgency = 'C-MEDIUM')
            self.assertIsNone(CrudTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CrudTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('C-MEDIUM', self.model_ticket_update.urgency)

            self.domain_ticket_update = Ticket(org_id = 'ORG002')
            self.assertIsNone(CrudTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CrudTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('ORG002', self.model_ticket_update.org_id)

            self.domain_ticket_update = Ticket(agent_id = 'AGT002')
            self.assertIsNone(CrudTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CrudTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('AGT002', self.model_ticket_update.agent_id)


    def test_d_delete_ticket_db(self):
        with DbHandler() as db:
            self.assertIsNone(CrudTicket.deleteTicket(db, self.domain_ticket.id))
            self.assertIsNone(CrudTicket.readTicketById(db, self.domain_ticket.id))
            self.assertIsNone(CrudAgent.deleteAgent(db, self.domain_agent.id))
            self.assertIsNone(CrudAgent.readAgentById(db, self.domain_agent.id))
            self.assertIsNone(CrudAgent.deleteAgent(db, self.domain_agent_update.id))
            self.assertIsNone(CrudAgent.readAgentById(db, self.domain_agent_update.id))
            self.assertIsNone(CrudOrganization.deleteOrganization(db, self.domain_org.id))
            self.assertIsNone(CrudOrganization.readOrganizationById(db, self.domain_org.id))
            self.assertIsNone(CrudOrganization.deleteOrganization(db, self.domain_org_update.id))
            self.assertIsNone(CrudOrganization.readOrganizationById(db, self.domain_org_update.id))



if __name__ == '__main__':
    unittest.main()

