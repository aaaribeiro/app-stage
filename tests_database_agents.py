import unittest
from database.handlers import DbHandler
from database.models import Agents as Model
from domain.agent import Agent as Domain
from crud.agent import Agent as CRUD


class TestAgentDB(unittest.TestCase):
    
    def setUp(self) -> None:
        self._id = 'IDXPTO01'


    def test_a_add_agent_db(self):
        with DbHandler() as db:
            self.agent = Domain(id=self._id, name='User Test',
                    team='BR-TEST')
            self.assertEqual(None, CRUD.createAgent(db, self.agent))

    
    def test_b_read_agent_db(self):
        with DbHandler() as db:
            self.model = CRUD.readAgentById(db, self._id)
            self.assertIsInstance(self.model, Model)
            self.assertEqual(self._id, self.model.id)
            self.assertEqual('User Test', self.model.name)
            self.assertEqual('BR-TEST', self.model.team)
    

    def test_c_update_agent_db(self):
        with DbHandler() as db:
            self.agent = Domain(name='Test User')
            self.assertEqual(None, CRUD.updateAgent(db, self.agent, self._id))
            self.model = CRUD.readAgentById(db, self._id)
            self.assertEqual('Test User', self.model.name)
            self.assertEqual('BR-TEST', self.model.team)


    def test_d_delete_agent_db(self):
        with DbHandler() as db:
            self.assertEqual(None, CRUD.deleteAgent(db, self._id))
            self.assertIsNone(CRUD.readAgentById(db, self._id))


if __name__ == '__main__':
    unittest.main()

