import unittest
from database.handlers import DbHandler
from database.models import Organizations as Model
from domain.organization import Organization as Domain
from crud.organization import Organization as CRUD


class TestOrgDB(unittest.TestCase):
    
    def setUp(self):
        self._id = 'IDORG001'
        self._name = 'Company Test'


    def test_a_add_org_db(self):
        with DbHandler() as db:
            self.domain = Domain(id=self._id, name=self._name)
            self.assertEqual(None, CRUD.createOrganization(db, self.domain))

    
    def test_b_read_org_db(self):
        with DbHandler() as db:
            self.model = CRUD.readOrganizationById(db, self._id)
            self.assertIsInstance(self.model, Model)
            self.assertEqual(self._id, self.model.id)
            self.assertEqual(self._name, self.model.name)
    

    def test_c_update_org_db(self):
        with DbHandler() as db:
            self.domain = Domain(name='Test Company')
            self.assertEqual(None, CRUD.updateOrganization(db, self.domain, self._id))
            self.model = CRUD.readOrganizationById(db, self._id)
            self.assertEqual('Test Company', self.model.name)


    def test_d_delete_org_db(self):
        with DbHandler() as db:
            self.assertEqual(None, CRUD.deleteOrganization(db, self._id))
            self.assertIsNone(CRUD.readOrganizationById(db, self._id))


if __name__ == '__main__':
    unittest.main()

