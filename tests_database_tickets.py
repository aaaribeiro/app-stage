import unittest
from datetime import datetime
from database.handlers import DbHandler
from database.models import Tickets as Model
from domain.ticket import TicketCreation as DomainCreation
# from domain.ticket import TicketUpdate as DomainUpdate
from domain.organization import Organization as DomainOrg
from domain.agent import Agent as DomainAgent
from crud.ticket import Ticket as CRUDTicket
from crud.agent import Agent as CRUDAgent
from crud.organization import Organization as CRUDOrg


class TestAgentDB(unittest.TestCase):
    
    def setUp(self):
        self.domain_org = DomainOrg(
            id = 'ORG001',
            name = 'ORG TEST'
        )

        self.domain_agent = DomainAgent(
            id = 'AGT001',
            name = 'AGENT TEST',
            team = 'BSS'
        )

        self.domain_ticket = DomainCreation(
        id = 1,
        org_id = 'ORG001',
        agent_id = 'AGT001',
        created_date = datetime.now(),
        status = 'NEW',
        category = 'HELP REQUEST',
        urgency = 'A-HIGH',
        subject = 'TTCKET TEST' 
        )


    def test_a_add_ticket_db(self):
        with DbHandler() as db:
            self.assertIsNone(CRUDOrg.createOrganization(db, self.domain_org))
            self.assertIsNone(CRUDAgent.createAgent(db, self.domain_agent))
            self.assertIsNone(CRUDTicket.createTicket(db, self.domain_ticket))
            

    
    # def test_b_read_ticket_db(self):
    #     with DbHandler() as db:
    #         self.model = CRUD.readAgentById(db, self._id)
    #         self.assertIsInstance(self.model, Model)
    #         self.assertEqual(self._id, self.model.id)
    #         self.assertEqual(self._name, self.model.name)
    #         self.assertEqual(self._team, self.model.team)
    

    # def test_c_update_ticket_db(self):
    #     with DbHandler() as db:
    #         self.domain = Domain(name='Test Agent')
    #         self.assertEqual(None, CRUD.updateAgent(db, self.domain, self._id))
    #         self.model = CRUD.readAgentById(db, self._id)
    #         self.assertEqual('Test Agent', self.model.name)
    #         self.assertEqual(self._team, self.model.team)


    def test_d_delete_ticket_db(self):
        with DbHandler() as db:
            self.assertIsNone(CRUDAgent.deleteAgent(db, self.domain_agent.id))
            self.assertIsNone(CRUDAgent.readAgentById(db, self.domain_agent.id))
            self.assertIsNone(CRUDOrg.deleteOrganization(db, self.domain_org.id))
            self.assertIsNone(CRUDOrg.readOrganizationById(db, self.domain_org.id))
            self.assertIsNone(CRUDTicket.deleteTicket(db, self.domain_ticket.id))
            self.assertIsNone(CRUDTicket.readTicketById(db, self.domain_ticket.id))


if __name__ == '__main__':
    unittest.main()

