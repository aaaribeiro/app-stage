import unittest
import requests
from datetime import datetime
from database.handlers import DbHandler
from database.models import Organizations as Model
from domain.organization import Organization as Domain
from crud.organization import Organization as CRUD


class TestTickettAPI(unittest.TestCase):
    
    def setUp(self):
        # self.url = 'https://app-stage-netcon.herokuapp.com/stage/movidesk/v1'
        self.url = 'http://localhost:8000/stage/movidesk/v1'

        self.ticket_request_body = {
            "id": 1,
            "org_id": "ORG001",
            "agent_id": "AGT001",
            "created_date": datetime.now().strftime("%Y-%m-%dT%H:%M:00"), #"%Y-%m-%dT%H:%M:%S.%fZ"
            "status": "NEW",
            "category": "HELP REQUEST",
            "urgency": "B-HIGH",
            "subject": "TTCKET TEST",
            "sla_solution_date": None,
            "sla_first_response": None
        }

        self.org_request_body = {
            'id': 'ORG001',
            'name': 'ORG TEST'
        }

        self.org_request_body_update = {
            'id': 'ORG002',
            'name': 'ORG UP-TO-DATE'
        }

        self.agent_request_body = {
            'id': 'AGT001',
            'name': 'AGENT TEST',
            'team': 'BSS'
        }

        self.agent_request_body_update = {
            'id': 'AGT002',
            'name': 'AGENT UP-TO-DATE',
            'team': 'BSS'
        }


    def test_a_add_org_api(self):
        response = requests.post(f'{self.url}/organizations', json=self.org_request_body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())
        response = requests.post(f'{self.url}/organizations', json=self.org_request_body_update)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())


    def test_b_add_agent_api(self):
        response = requests.post(f'{self.url}/agents', json=self.agent_request_body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())
        response = requests.post(f'{self.url}/agents', json=self.agent_request_body_update)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())

    
    def test_c_add_ticket_api(self):
        response = requests.post(f'{self.url}/tickets', json=self.ticket_request_body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())
        # adding same ticket twice
        response = requests.post(f'{self.url}/tickets', json=self.ticket_request_body)
        self.assertEqual(400, response.status_code)


    def test_d_read_ticket_api(self):
        response = requests.get(f"{self.url}/tickets/{self.ticket_request_body['id']}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.ticket_request_body, response.json())
        response = requests.get(f"{self.url}/99999")
        self.assertEqual(response.status_code, 404)
    

    def test_e_basic_update_ticket_db(self):
        payload = {'status': 'IN PROGRESS'}
        response = requests.patch(f"{self.url}/tickets/{self.ticket_request_body['id']}",
                                json=payload)
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.json())
        response = requests.get(f"{self.url}/tickets/{self.ticket_request_body['id']}", json=payload)
        self.assertEqual(payload["status"], response.json()["status"])
    
        payload = {'category': 'INCIDENT', 'urgency': 'C-MEDIUM'}
        response = requests.patch(f"{self.url}/tickets/{self.ticket_request_body['id']}",
                                json=payload)
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.json())
        response = requests.get(f"{self.url}/tickets/{self.ticket_request_body['id']}", json=payload)
        self.assertEqual(payload["category"], response.json()["category"])
        self.assertEqual(payload["urgency"], response.json()["urgency"])



    def test_f_advanced_update_ticket_api(self):
        payload = {'org_id': self.org_request_body_update['id']}
        response = requests.patch(f"{self.url}/tickets/{self.ticket_request_body['id']}",
                                json=payload)
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.json())
        response = requests.get(f"{self.url}/tickets/{self.ticket_request_body['id']}", json=payload)
        self.assertEqual(payload["org_id"], response.json()["org_id"])

        payload = {'agent_id': self.agent_request_body_update['id'], 'urgency': 'D-LOW'}
        response = requests.patch(f"{self.url}/tickets/{self.ticket_request_body['id']}",
                                json=payload)
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.json())
        response = requests.get(f"{self.url}/tickets/{self.ticket_request_body['id']}", json=payload)
        self.assertEqual(payload["agent_id"], response.json()["agent_id"])
        self.assertEqual(payload["urgency"], response.json()["urgency"])

        payload = {'agent_id': 'IDNOTFOUND'}
        response = requests.patch(f"{self.url}/tickets/{self.ticket_request_body['id']}",
                                json=payload)
        self.assertEqual(404, response.status_code)
        self.assertEqual('agent not found', response.json()['detail'])

        payload = {'org_id': 'IDNOTFOUND'}
        response = requests.patch(f"{self.url}/tickets/{self.ticket_request_body['id']}",
                                json=payload)
        self.assertEqual(404, response.status_code)
        self.assertEqual('organization not found', response.json()['detail'])


    def test_g_delete_ticket_api(self):
        response = requests.delete(f"{self.url}/tickets/{self.ticket_request_body['id']}")
        self.assertEqual(200, response.status_code)
        # deleting same ticket twice
        response = requests.delete(f"{self.url}/tickets/{self.ticket_request_body['id']}")
        self.assertEqual(404, response.status_code)


    def test_h_delete_agent_api(self):
        response = requests.delete(f"{self.url}/agents/{self.agent_request_body['id']}")
        self.assertEqual(200, response.status_code)
        response = requests.delete(f"{self.url}/agents/{self.agent_request_body_update['id']}")
        self.assertEqual(200, response.status_code)
    

    def test_i_delete_org_api(self):    
        response = requests.delete(f"{self.url}/organizations/{self.org_request_body['id']}")
        self.assertEqual(200, response.status_code)
        response = requests.delete(f"{self.url}/organizations/{self.org_request_body_update['id']}")
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()

