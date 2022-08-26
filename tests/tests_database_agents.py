import sys
import os.path
sys.path.insert(0, os.path.abspath('.'))

import unittest
from app.database.dbHandlers import DbHandler
from app.database.models import Agents as Model
from app.database.crud.crudAgent import CrudAgent
from app.domain.agent import Agent


class TestAgentDB(unittest.TestCase):
    
    def setUp(self):
        self._id = 'AGT001'
        self._name = 'AGENT TEST'
        self._team = 'BSS'


    def test_a_add_agent_db(self):
        with DbHandler() as db:
            self.domain = Agent(id=self._id, name=self._name,
                    team=self._team)
            self.assertEqual(None, CrudAgent.createAgent(db, self.domain))

    
    def test_b_read_agent_db(self):
        with DbHandler() as db:
            self.model = CrudAgent.readAgentById(db, self._id)
            self.assertIsInstance(self.model, Model)
            self.assertEqual(self._id, self.model.id)
            self.assertEqual(self._name, self.model.name)
            self.assertEqual(self._team, self.model.team)
    

    def test_c_update_agent_db(self):
        with DbHandler() as db:
            self.domain = Agent(name='AGENT UP-TO-DATE')
            self.assertEqual(None, CrudAgent.updateAgent(db, self.domain, self._id))
            self.model = CrudAgent.readAgentById(db, self._id)
            self.assertEqual('AGENT UP-TO-DATE', self.model.name)
            self.assertEqual(self._team, self.model.team)


    def test_d_delete_agent_db(self):
        with DbHandler() as db:
            self.assertEqual(None, CrudAgent.deleteAgent(db, self._id))
            self.assertIsNone(CrudAgent.readAgentById(db, self._id))


if __name__ == '__main__':
    unittest.main()

