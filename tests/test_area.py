import os, pytest, logging, unittest
from main import app
from database import create_db
from models import Locker, Area
from controllers import (
    add_new_area,
    delete_area,
    get_area_by_id,
    get_area_all,
    set_description,
    set_latitude,
    set_longitude,
)

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

@pytest.fixture(autouse=True, scope="class")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"//py_test.db")

class AreaIntegratedTests (unittest.TestCase):
    def test_add_new_area(self):
        new_area = add_new_area('A1001','A locker description',10.283759,-61.404937)
        assert new_area.id == 1
        assert new_area.locker_id == 'A1001'
        assert new_area.longitude == 10.283759        
        assert new_area.latitude == -61.404937
        assert new_area.description == 'A locker description'

    def test_add_new_area_duplicate(self):
        new_area = add_new_area('A1001','A locker description',10.283759,-61.404937)
        self.assertIsNone(new_area)
    
    def test_get_area_by_id(self):
        area = get_area_by_id(1)
        assert area.id == 1
        assert area.locker_id == 'A1001'
        assert area.longitude == 10.283759        
        assert area.latitude == -61.404937
        assert area.description == 'A locker description'

    def test_get_area_by_id_invalid(self):
        area = get_area_by_id(0)
        self.assertIsNone(area)
    
    def test_set_description(self):
        area = set_description(1,'A new locker description')
        assert area.description == 'A new locker description'
    
    def test_set_description_invalid(self):
        area = set_description(0,'A invalid locker description')
        self.assertIsNone(area)
    
    def test_set_latitude(self):
        area = set_latitude(1,9.47893)
        assert area.latitude == 9.47893
    
    def test_set_latitude_invalid(self):
        area = set_latitude(0,9.47893)
        self.assertIsNone(area)

    def test_set_longitude(self):
        area = set_longitude(1,-99.40400)
        assert area.longitude == -99.40400

    def test_set_longitude_invalid(self):
        area = set_longitude(0,-99.40400)
        self.assertIsNone(area)
    
    def test_delete_area(self):
        add_new_area('A1111','A locker description',45.85739, -25.45543)
        area = delete_area(2)
        self.assertIsNotNone(area)
        self.assertIsNone(get_area_by_id(2))
    
    def test_delete_area_invalid(self):
        area = delete_area(2)
        self.assertIsNone(area)
    
    def test_get_all_area(self):
        results =  get_area_all()
        expectedList = [{
            'id':1,
            'locker_id':'A1001',
            'description':'A locker description',
            'longitude': 10.283759,
            'latitude': -61.404937
        }]
        self.assertListEqual(expectedList,results)




        
