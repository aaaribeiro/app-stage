import unittest
import requests
from database.handlers import DbHandler
from database.models import Agents as Model
from domain.agent import Agent as Domain
from crud.agent import Agent as CRUD


class TestAgentAPI(unittest.TestCase):
    
    def setUp(self):
        self.url = 'https://app-stage-netcon.herokuapp.com/stage/movidesk/v1/agents'
        self.request_body = {
            'id': 'IDORG001',
            'name': 'Agent Test',
            'team': 'BR-TEST'
        }


    def test_a_add_agent_api(self):
        response = requests.post(self.url, json=self.request_body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())


    def test_b_read_agent_api(self):
        response = requests.get(f"{self.url}/{self.request_body['id']}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.request_body, response.json())
        response = requests.get(f"{self.url}/IDNOTFOUND")
        self.assertEqual(404, response.status_code)
    

    def test_c_update_agent_db(self):
        payload = {
            'name': 'Test Agent'
        }
        response_expected = {
            'id': 'IDORG001',
            'name': 'Test Agent',
            'team': 'BR-TEST'
        }
        response = requests.patch(f"{self.url}/{self.request_body['id']}",
                                json=payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual(None, response.json())
        response = requests.get(f"{self.url}/{self.request_body['id']}")
        self.assertEqual(response_expected, response.json())


    def test_d_delete_agent_api(self):
        response = requests.delete(f"{self.url}/{self.request_body['id']}")
        self.assertEqual(200, response.status_code)
        response = requests.delete(f"{self.url}/IDNOTFOUND")
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()

