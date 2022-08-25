import unittest
from datetime import datetime, timedelta
from database.handlers import DbHandler
from database.models import TimeAppointments as Model
from domain.timeAppointment import TimeAppointment as Domain
from domain.agent import Agent as DomainAgent
from domain.ticket import TicketUpdate as DomainCreation
from domain.organization import Organization as DomainOrg
from crud.timeAppointment import TimeAppointment as CRUD
from crud.ticket import Ticket as CRUDTicket
from crud.agent import Agent as CRUDAgent
from crud.organization import Organization as CRUDOrg



class TestTimeAppointmentDB(unittest.TestCase):
    
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
            urgency = 'B-HIGH',
            subject = 'TTCKET TEST' 
        )

        self.domain_time_appointment = Domain(
            id = 1,
            ticket_id = 1,
            agent_id = 'AGT001',
            time_appointment = str(timedelta(hours=1)),
            created_date = datetime.now()
        )
        

    def test_a_add_time_appointment_db(self):
        with DbHandler() as db:
            self.assertIsNone(CRUDOrg.createOrganization(db, self.domain_org))
            self.assertIsNone(CRUDAgent.createAgent(db, self.domain_agent))
            self.assertIsNone(CRUDTicket.createTicket(db, self.domain_ticket))
            self.assertIsNone(CRUD.createTimeAppointment(db, self.domain_time_appointment))
    

    def test_b_read_time_appointment_db(self):
        with DbHandler() as db:
            self.model_time_appointment = CRUD.readTimeAppointmentById(db, self.domain_ticket.id)
            self.model_time_appointment_expected = Model()
            for attr in self.domain_time_appointment.fields_set():
                setattr(self.model_time_appointment_expected,
                        attr, getattr(self.domain_time_appointment, attr))
            self.domain_time_appointment_expected = Domain.from_orm(self.model_time_appointment_expected)
            self.assertIsInstance(self.model_time_appointment, Model)
            self.assertEqual(self.domain_time_appointment_expected, self.domain_time_appointment)


    def test_c_update_time_appointment_db(self):
        with DbHandler() as db:
            self.domain_time_appointment_update = Domain(time_appointment = str(timedelta(hours=2)))
            self.assertIsNone(CRUD.updateTimeAppointment(db, self.domain_time_appointment_update,
                            self.domain_time_appointment.id))
            self.model_time_appointment_update = CRUD.readTimeAppointmentById(db, self.domain_ticket.id)
            self.assertEqual('02:00:00', str(self.model_time_appointment_update.time_appointment))


    def test_d_delete_time_appointment_db(self):
        with DbHandler() as db:
            self.assertIsNone(CRUD.deleteTimeAppointment(db, self.domain_time_appointment.id))
            self.assertIsNone(CRUD.readTimeAppointmentById(db, self.domain_time_appointment.id))
            self.assertIsNone(CRUDTicket.deleteTicket(db, self.domain_ticket.id))
            self.assertIsNone(CRUDTicket.readTicketById(db, self.domain_ticket.id))
            self.assertIsNone(CRUDAgent.deleteAgent(db, self.domain_agent.id))
            self.assertIsNone(CRUDAgent.readAgentById(db, self.domain_agent.id))
            self.assertIsNone(CRUDOrg.deleteOrganization(db, self.domain_org.id))
            self.assertIsNone(CRUDOrg.readOrganizationById(db, self.domain_org.id))


if __name__ == '__main__':
    unittest.main()

