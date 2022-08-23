import unittest
from database.handlers import DbHandler
from database.models import Agents as Model
from domain.agent import Agent as Domain
from crud.agent import Agent as CRUD


class TestAgentDB(unittest.TestCase):
    
    def setUp(self):
        self._id = 'IDXPTO01'
        self._name = 'Agent Test'
        self._team = 'BR-TEST'


    def test_a_add_agent_db(self):
        with DbHandler() as db:
            self.domain = Domain(id=self._id, name=self._name,
                    team=self._team)
            self.assertEqual(None, CRUD.createAgent(db, self.domain))

    
    def test_b_read_agent_db(self):
        with DbHandler() as db:
            self.model = CRUD.readAgentById(db, self._id)
            self.assertIsInstance(self.model, Model)
            self.assertEqual(self._id, self.model.id)
            self.assertEqual(self._name, self.model.name)
            self.assertEqual(self._team, self.model.team)
    

    def test_c_update_agent_db(self):
        with DbHandler() as db:
            self.domain = Domain(name='Test Agent')
            self.assertEqual(None, CRUD.updateAgent(db, self.domain, self._id))
            self.model = CRUD.readAgentById(db, self._id)
            self.assertEqual('Test Agent', self.model.name)
            self.assertEqual(self._team, self.model.team)


    def test_d_delete_agent_db(self):
        with DbHandler() as db:
            self.assertEqual(None, CRUD.deleteAgent(db, self._id))
            self.assertIsNone(CRUD.readAgentById(db, self._id))


if __name__ == '__main__':
    unittest.main()

