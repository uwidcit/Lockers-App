import os, pytest, logging, unittest
from models import Locker

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
