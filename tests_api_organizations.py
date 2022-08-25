import unittest
import requests


class TestAgentAPI(unittest.TestCase):
    
    def setUp(self):
        # self.url = 'https://app-stage-netcon.herokuapp.com/stage/movidesk/v1/organizations'
        self.url = 'http://localhost:8000/stage/movidesk/v1/organizations'
        self.request_body = {
            'id': 'ORG001',
            'name': 'ORG TEST'
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
        payload = {'name': 'ORG UP-TO-DATE'}
        response = requests.patch(f"{self.url}/{self.request_body['id']}",
                                json=payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual(None, response.json())
        response = requests.get(f"{self.url}/{self.request_body['id']}")
        self.assertEqual(payload["name"], response.json()["name"])


    def test_d_delete_org_api(self):
        response = requests.delete(f"{self.url}/{self.request_body['id']}")
        self.assertEqual(200, response.status_code)
        response = requests.delete(f"{self.url}/IDNOTFOUND")
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()

