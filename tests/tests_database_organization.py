import sys
import os.path
sys.path.insert(0, os.path.abspath('.'))

import unittest
from app.database.dbHandlers import DbHandler
from app.database.models import Organizations
from app.domain.organization import Organization
from app.database.crud.crudOrganization import CrudOrganization


class TestOrgDB(unittest.TestCase):
    
    def setUp(self):
        self._id = 'ORG001'
        self._name = 'ORG TEST'


    def test_a_add_org_db(self):
        with DbHandler() as db:
            self.domain = Organization(id=self._id, name=self._name)
            self.assertEqual(None,
                CrudOrganization.createOrganization(db, self.domain))

    
    def test_b_read_org_db(self):
        with DbHandler() as db:
            self.model = CrudOrganization.readOrganizationById(db, self._id)
            self.assertIsInstance(self.model, Organizations)
            self.assertEqual(self._id, self.model.id)
            self.assertEqual(self._name, self.model.name)
    

    def test_c_update_org_db(self):
        with DbHandler() as db:
            self.domain = Organization(name='ORG UP-TO-DATE')
            self.assertEqual(None,
                CrudOrganization.updateOrganization(db, self.domain, self._id))
            self.model = CrudOrganization.readOrganizationById(db, self._id)
            self.assertEqual('ORG UP-TO-DATE', self.model.name)


    def test_d_delete_org_db(self):
        with DbHandler() as db:
            self.assertEqual(None,
                CrudOrganization.deleteOrganization(db, self._id))
            self.assertIsNone(CrudOrganization.readOrganizationById(db, self._id))


if __name__ == '__main__':
    unittest.main()

