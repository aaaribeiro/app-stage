import unittest
import requests
from database.handlers import DbHandler
from database.models import Organizations as Model
from domain.organization import Organization as Domain
from crud.organization import Organization as CRUD


class TestAgentAPI(unittest.TestCase):
    
    def setUp(self):
        self.url = 'https://app-stage-netcon.herokuapp.com/stage/movidesk/v1/organizations'
        self.request_body = {
            'id': 'IDORG001',
            'name': 'Test Company'
        }


    def test_a_add_org_api(self):
        response = requests.post(self.url, json=self.request_body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())


    def test_b_read_org_api(self):
        response = requests.get(f"{self.url}/{self.request_body['id']}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.request_body, response.json())
        response = requests.get(f"{self.url}/IDNOTFOUND")
        self.assertEqual(response.status_code, 404)
    

    def test_c_update_org_db(self):
        payload = {
            'name': 'Company Test'
        }
        response_expected = {
            'id': 'IDORG001',
            'name': 'Company Test'
        }
        response = requests.patch(f"{self.url}/{self.request_body['id']}",
                                json=payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual(None, response.json())
        response = requests.get(f"{self.url}/{self.request_body['id']}")
        self.assertEqual(response_expected, response.json())


    def test_d_delete_org_api(self):
        response = requests.delete(f"{self.url}/{self.request_body['id']}")
        self.assertEqual(200, response.status_code)
        response = requests.delete(f"{self.url}/IDNOTFOUND")
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()

