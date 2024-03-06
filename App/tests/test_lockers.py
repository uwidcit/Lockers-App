import os, pytest, logging, unittest
from App.main import create_app
from App.database import create_db
from App.models import Locker
from App.models.locker import LockerStatus,LockerTypes 
from App.controllers import (
    add_new_locker,
    get_lockers_available,
    get_locker_id,
    get_all_lockers,
    getLockerTypes,
    getStatuses,
    rent_locker,
    release_locker,
    delete_locker,
    update_key,
    update_locker_type,
    update_locker_status
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class LockerUnitTests(unittest.TestCase):

    def test_new_locker(self):
        new_locker = Locker('A1001','MEDIUM','FREE','AVAILABLE')
        assert new_locker.locker_code =='A1001' 
        assert new_locker.locker_type.value == 'Medium' 
        assert new_locker.status.value == 'Free'
        assert new_locker.key.value == 'Available'

    def test_new_locker_toJSON(self):
        new_locker = Locker('A2010','SMALL','RENTED','UNAVAILABLE')

        expected_json = {
            'locker_code':'A2010',
            'locker_type':'Small',
            'status':'Rented',
            'key': 'Unavailable',
            'area': []
            }
        self.assertDictEqual(new_locker.toJSON(),expected_json)

@pytest.fixture(autouse=True, scope="class")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"//py_test.db")

class LockerIntegrationTests(unittest.TestCase):
    def test_add_new_locker(self):
        new_locker = add_new_locker('A1001','MEDIUM','FREE','AVAILABLE')
        self.assertIsNotNone(new_locker)
        assert new_locker.locker_code =='A1001' 
        assert new_locker.locker_type.value == 'Medium' 
        assert new_locker.status.value == 'Free'
        assert new_locker.key.value == 'Available'
    
    def test_add_new_locker_duplicate(self):
        new_locker = add_new_locker('A1001','MEDIUM','FREE','AVAILABLE')
        self.assertIsNone(new_locker)
    
    def test_get_available_lockers(self):
        result = get_lockers_available()
        expected_list = [{
            'locker_code':'A1001',
            'locker_type':'Medium',
            'status':'Free',
            'key': 'Available',
            'area': []
            }]
        self.assertListEqual(expected_list, result)
    
    def test_get_all_lockers(self):
        result = get_all_lockers()
        expected_list = [{
            'locker_code':'A1001',
            'locker_type':'Medium',
            'status':'Free',
            'key': 'Available',
            'area': []
            }]
        self.assertListEqual(expected_list, result)

    def test_rent_locker(self):
        result = rent_locker('A1001')
        self.assertTrue(result)
        locker = get_locker_id('A1001')
        assert locker.status == Status.RENTED

    def test_rent_locker_rented(self):
        result = rent_locker('A1001')
        self.assertIsNone(result)
    
    def test_rent_locker_invalid(self):
        result = rent_locker('A1241')
        self.assertIsNone(result)

    def test_release_locker(self):
        result = release_locker('A1001')
        self.assertTrue(result)
        locker = get_locker_id('A1001')
        assert locker.status == Status.FREE
    
    def test_release_locker_invalid(self):
        result = release_locker('A1241')
        self.assertIsNone(result)
    
    def test_delete_locker(self):
        add_new_locker('A1111','COMBINATION','RENTED','UNAVAILABLE')
        locker = delete_locker('A1111')
        self.assertIsNotNone(locker)
        self.assertIsNone(get_locker_id('A1111'))
    
    def test_delete_locker_invalid(self):
        result = delete_locker('A1241')
        self.assertIsNone(result)

    def test_update_key_unavailble(self):
         locker = update_key('A1001','Unavailable')
         assert locker.key == Key.UNAVAILABLE

    def test_update_key_Lost(self):
         locker = update_key('A1001','Lost')
         assert locker.key == Key.LOST

    def test_update_key_available(self):
         locker = update_key('A1001','available')
         assert locker.key == Key.AVAILABLE

    def test_update_key_invalidLocker(self):
         locker = update_key('A1111','Unavailable')
         self.assertIsNone(locker)

    def test_update_key_invalidKeyStatus(self):
         locker = update_key('A1001','Not available')
         self.assertIsNone(locker)

    def test_update_locker_type_small(self):
         locker = update_locker_type('A1001','Small')
         assert locker.locker_type == LockerTypes.SMALL

    def test_update_locker_type_combination(self):
         locker = update_locker_type('A1001','Combination')
         assert locker.locker_type == LockerTypes.COMBINATION

    def test_update_locker_type_medium(self):
         locker = update_locker_type('A1001','Medium')
         assert locker.locker_type == LockerTypes.MEDIUM

    def test_update_locker_type_invalid(self):
         locker = update_locker_type('A1001','Large')
         self.assertIsNone(locker)

    def test_update_locker_status_rented (self):
         locker = update_locker_status('A1001','Rented')
         assert locker.status == Status.RENTED
    
    def test_update_locker_status_repair (self):
         locker = update_locker_status('A1001','Repair')
         assert locker.status == Status.REPAIR

    def test_update_locker_status_free (self):
         locker = update_locker_status('A1001','Free')
         assert locker.status == Status.FREE
    
    def test_update_locker_status_invalid (self):
         locker = update_locker_status('A1001','Broken')
         self.assertIsNone(locker)
    
    def test_getStatuses(self):
        expectedList =['Rented','Repair','Free']
        result = getStatuses()
        self.assertListEqual(expectedList,result)
    
    def test_getLockerTypes(self):
        expectedList =['Small','Medium','Combination']
        result = getLockerTypes()
        self.assertListEqual(expectedList,result)
