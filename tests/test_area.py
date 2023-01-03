import os, pytest, logging, unittest
from models import Locker, Area

LOGGER = logging.getLogger(__name__)

class AreaUnitTests(unittest.TestCase):
    def test_new_area(self):
        new_locker = Locker('A1001','MEDIUM','FREE','AVAILABLE')
        new_area = Area(new_locker.locker_code,'A locker description',10.283759,-61.404937)
        assert new_area.locker_id == 'A1001'
        assert new_area.longitude == 10.283759        
        assert new_area.latitude == -61.404937
        assert new_area.description == 'A locker description'

    def test_new_area_toJSON(self):
        new_locker = Locker('A2010','SMALL','RENTED','UNAVAILABLE')
        new_area = Area(new_locker.locker_code,'A locker description',10.259674,-61.411548)

        expected_json = {
            'id':None,
            'locker_id':'A2010',
            'description':'A locker description',
            'longitude': 10.259674,
            'latitude': -61.411548
        }
        self.assertDictEqual(expected_json,new_area.toJSON())
        
