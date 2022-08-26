import unittest
import requests
from datetime import datetime


class TestTimeAppintmenttAPI(unittest.TestCase):
    
    def setUp(self):
        # self.url = 'https://app-stage-netcon.herokuapp.com/stage/movidesk/v1'
        self.url = 'http://localhost:8000/stage/movidesk/v1'

        self.time_appointment_request_body ={
            'id': 1,
            'agent_id': 'AGT001',
            'ticket_id': 1,
            'time_appointment': '01:00:00', #str(timedelta(hours=1))
            'created_date': datetime.now().strftime("%Y-%m-%dT%H:%M:00") #datetime.now().strftime("%Y-%m-%dT%H:%M:00")
        }
        
        self.ticket_request_body = {
            'id': 1,
            'org_id': 'ORG001',
            'agent_id': 'AGT001',
            'created_date': datetime.now().strftime('%Y-%m-%dT%H:%M:00'), #%Y-%m-%dT%H:%M:%S.%fZ
            'status': 'NEW',
            'category': 'HELP REQUEST',
            'urgency': 'B-HIGH',
            'subject': 'TTCKET TEST',
            'sla_solution_date': None,
            'sla_first_response': None
        }

        self.org_request_body = {
            'id': 'ORG001',
            'name': 'ORG TEST'
        }


        self.agent_request_body = {
            'id': 'AGT001',
            'name': 'AGENT TEST',
            'team': 'BSS'
        }


    def test_a_add_organization_api(self):
        response = requests.post(f'{self.url}/organizations', json=self.org_request_body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())


    def test_b_add_agent_api(self):
        response = requests.post(f'{self.url}/agents', json=self.agent_request_body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())

    
    def test_c_add_ticket_api(self):
        response = requests.post(f'{self.url}/tickets', json=self.ticket_request_body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())
    

    def test_d_add_time_appointment_api(self):
        response = requests.post(f'{self.url}/timeappointments',
                                json=self.time_appointment_request_body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())
        # adding same appointment twice
        response = requests.post(f'{self.url}/timeappointments',
                                json=self.time_appointment_request_body)
        self.assertEqual(400, response.status_code)


    def test_e_read_time_appointment_api(self):
        response = requests.get(f"{self.url}/timeappointments/{self.time_appointment_request_body['id']}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.time_appointment_request_body, response.json())
        response = requests.get(f"{self.url}/timeappointments/0")
        self.assertEqual(response.status_code, 404)
    

    def test_f_basic_update_ticket_db(self):
        payload = {'time_appointment': '02:00:00'}
        response = requests.patch(f"{self.url}/timeappointments/{self.ticket_request_body['id']}",
                                json=payload)
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.json())
        response = requests.get(f"{self.url}/timeappointments/{self.ticket_request_body['id']}", json=payload)
        self.assertEqual(payload["time_appointment"], response.json()["time_appointment"])
    

    def test_g_advanced_update_ticket_api(self):
        payload = {'agent_id': 'IDNOTFOUND'}
        response = requests.patch(f"{self.url}/timeappointments/{self.time_appointment_request_body['id']}",
                                json=payload)
        self.assertEqual(404, response.status_code)
        self.assertEqual('agent not found', response.json()['detail'])

        payload = {'ticket_id': 99999}
        response = requests.patch(f"{self.url}/timeappointments/{self.time_appointment_request_body['id']}",
                                json=payload)
        self.assertEqual(404, response.status_code)
        self.assertEqual('ticket not found', response.json()['detail'])


    def test_h_delete_time_appointment_api(self):
        response = requests.delete(f"{self.url}/timeappointments/{self.time_appointment_request_body['id']}")
        self.assertEqual(200, response.status_code)
        # deleting same appointment twice
        response = requests.delete(f"{self.url}/timeappointments/{self.time_appointment_request_body['id']}")
        self.assertEqual(404, response.status_code)
    

    def test_i_delete_ticket_api(self):
        response = requests.delete(f"{self.url}/tickets/{self.ticket_request_body['id']}")
        self.assertEqual(200, response.status_code)


    def test_j_delete_agent_api(self):
        response = requests.delete(f"{self.url}/agents/{self.agent_request_body['id']}")
        self.assertEqual(200, response.status_code)


    def test_l_delete_org_api(self):    
        response = requests.delete(f"{self.url}/organizations/{self.org_request_body['id']}")
        self.assertEqual(200, response.status_code)



if __name__ == '__main__':
    unittest.main()

