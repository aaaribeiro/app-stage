import sys
import os.path
sys.path.insert(0, os.path.abspath('.'))

import unittest
from datetime import datetime, timedelta
from app.database.dbHandlers import DbHandler
from app.database.models import TimeAppointments
from app.domain.appointment import TimeAppointment
from app.domain.agent import Agent
from app.domain.ticket import Ticket
from app.domain.organization import Organization
from app.database.crud.crudAppointment import CrudTimeAppointment
from app.database.crud.crudTicket import CrudTicket
from app.database.crud.crudAgent import CrudAgent
from app.database.crud.crudOrganization import CrudOrganization



class TestTimeAppointmentDB(unittest.TestCase):
    
    def setUp(self):
        self.domain_org = Organization(
            id = 'ORG001',
            name = 'ORG TEST'
        )

        self.domain_agent = Agent(
            id = 'AGT001',
            name = 'AGENT TEST',
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

        self.domain_time_appointment = TimeAppointment(
            id = 1,
            ticket_id = 1,
            agent_id = 'AGT001',
            time_appointment = str(timedelta(hours=1)),
            created_date = datetime.now()
        )
        

    def test_a_add_time_appointment_db(self):
        with DbHandler() as db:
            self.assertIsNone(CrudOrganization.createOrganization(
                db,self.domain_org))
            self.assertIsNone(CrudAgent.createAgent(db, self.domain_agent))
            self.assertIsNone(CrudTicket.createTicket(db, self.domain_ticket))
            self.assertIsNone(CrudTimeAppointment.createTimeAppointment(
                db, self.domain_time_appointment))
    

    def test_b_read_time_appointment_db(self):
        with DbHandler() as db:
            self.model_time_appointment = CrudTimeAppointment.readTimeAppointmentById(
                db, self.domain_ticket.id)
            self.model_time_appointment_expected = TimeAppointments()
            for attr in self.domain_time_appointment.fields_set():
                setattr(self.model_time_appointment_expected,
                        attr, getattr(self.domain_time_appointment, attr))
            self.domain_time_appointment_expected = TimeAppointment.from_orm(
                self.model_time_appointment_expected)
            self.assertIsInstance(self.model_time_appointment, TimeAppointments)
            self.assertEqual(self.domain_time_appointment_expected, self.domain_time_appointment)


    def test_c_update_time_appointment_db(self):
        with DbHandler() as db:
            self.domain_time_appointment_update = TimeAppointment(
                time_appointment = str(timedelta(hours=2)))
            self.assertIsNone(CrudTimeAppointment.updateTimeAppointment(
                db, self.domain_time_appointment_update, self.domain_time_appointment.id))
            self.model_time_appointment_update = CrudTimeAppointment.readTimeAppointmentById(
                db, self.domain_ticket.id)
            self.assertEqual('02:00:00',
                str(self.model_time_appointment_update.time_appointment))


    def test_d_delete_time_appointment_db(self):
        with DbHandler() as db:
            self.assertIsNone(CrudTimeAppointment.deleteTimeAppointment(
                db, self.domain_time_appointment.id))
            self.assertIsNone(CrudTimeAppointment.readTimeAppointmentById(
                db, self.domain_time_appointment.id))
            self.assertIsNone(CrudTicket.deleteTicket(db, self.domain_ticket.id))
            self.assertIsNone(CrudTicket.readTicketById(db, self.domain_ticket.id))
            self.assertIsNone(CrudAgent.deleteAgent(db, self.domain_agent.id))
            self.assertIsNone(CrudAgent.readAgentById(db, self.domain_agent.id))
            self.assertIsNone(CrudOrganization.deleteOrganization(db, self.domain_org.id))
            self.assertIsNone(CrudOrganization.readOrganizationById(db, self.domain_org.id))


if __name__ == '__main__':
    unittest.main()

