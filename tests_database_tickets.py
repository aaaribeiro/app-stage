import unittest
from datetime import datetime
from database.handlers import DbHandler
from database.models import Tickets as Model
from domain.ticket import TicketCreation as DomainCreation
from domain.ticket import TicketUpdate as DomainUpdate
from domain.organization import Organization as DomainOrg
from domain.agent import Agent as DomainAgent
from crud.ticket import Ticket as CRUDTicket
from crud.agent import Agent as CRUDAgent
from crud.organization import Organization as CRUDOrg


class TestTicketDB(unittest.TestCase):
    
    def setUp(self):
        self.domain_org = DomainOrg(
            id = 'ORG001',
            name = 'ORG TEST'
        )

        self.domain_org_update = DomainOrg(
            id = 'ORG002',
            name = 'ORG UP-TO-DATE'
        )

        self.domain_agent = DomainAgent(
            id = 'AGT001',
            name = 'AGENT TEST',
            team = 'BSS'
        )

        self.domain_agent_update = DomainAgent(
                id = 'AGT002',
                name = 'AGENT UP-TO-DATE',
                team = 'BSS'
        )

        self.domain_ticket = DomainCreation(
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
            self.assertIsNone(CRUDOrg.createOrganization(db, self.domain_org))
            self.assertIsNone(CRUDOrg.createOrganization(db, self.domain_org_update))
            self.assertIsNone(CRUDAgent.createAgent(db, self.domain_agent))
            self.assertIsNone(CRUDAgent.createAgent(db, self.domain_agent_update))
            self.assertIsNone(CRUDTicket.createTicket(db, self.domain_ticket))
            
    
    def test_b_read_ticket_db(self):
        with DbHandler() as db:
            self.model_ticket = CRUDTicket.readTicketById(db, self.domain_ticket.id)
            self.model_ticket_expected = CRUDTicket()
            for attr in self.domain_ticket.fields_set():
                setattr(self.model_ticket_expected, attr, getattr(self.domain_ticket, attr))
            self.domain_expected = DomainCreation.from_orm(self.model_ticket_expected)
            self.assertIsInstance(self.model_ticket, Model)
            self.assertEqual(self.domain_expected, self.domain_ticket)


    def test_c_update_ticket_db(self):
        with DbHandler() as db:
            self.domain_ticket_update = DomainUpdate(status = 'IN PROGRESS')
            self.assertIsNone(CRUDTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CRUDTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('IN PROGRESS', self.model_ticket_update.status)

            self.domain_ticket_update = DomainUpdate(category = 'INCIDENT')
            self.assertIsNone(CRUDTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CRUDTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('INCIDENT', self.model_ticket_update.category)

            self.domain_ticket_update = DomainUpdate(urgency = 'C-MEDIUM')
            self.assertIsNone(CRUDTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CRUDTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('C-MEDIUM', self.model_ticket_update.urgency)

            self.domain_ticket_update = DomainUpdate(org_id = 'ORG002')
            self.assertIsNone(CRUDTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CRUDTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('ORG002', self.model_ticket_update.org_id)

            self.domain_ticket_update = DomainUpdate(agent_id = 'AGT002')
            self.assertIsNone(CRUDTicket().updateTicket(db, self.domain_ticket_update, self.domain_ticket.id))
            self.model_ticket_update = CRUDTicket.readTicketById(db, self.domain_ticket.id)
            self.assertEqual('AGT002', self.model_ticket_update.agent_id)


    def test_d_delete_ticket_db(self):
        with DbHandler() as db:
            self.assertIsNone(CRUDTicket.deleteTicket(db, self.domain_ticket.id))
            self.assertIsNone(CRUDTicket.readTicketById(db, self.domain_ticket.id))
            self.assertIsNone(CRUDAgent.deleteAgent(db, self.domain_agent.id))
            self.assertIsNone(CRUDAgent.readAgentById(db, self.domain_agent.id))
            self.assertIsNone(CRUDAgent.deleteAgent(db, self.domain_agent_update.id))
            self.assertIsNone(CRUDAgent.readAgentById(db, self.domain_agent_update.id))
            self.assertIsNone(CRUDOrg.deleteOrganization(db, self.domain_org.id))
            self.assertIsNone(CRUDOrg.readOrganizationById(db, self.domain_org.id))
            self.assertIsNone(CRUDOrg.deleteOrganization(db, self.domain_org_update.id))
            self.assertIsNone(CRUDOrg.readOrganizationById(db, self.domain_org_update.id))



if __name__ == '__main__':
    unittest.main()

