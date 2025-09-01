import os, pytest, logging, unittest
from App.main import create_app
from App.database import create_db
from App.models import Locker, Area
from App.controllers import (
    add_new_area,
    add_new_locker,
    delete_area,
    get_area_by_id,
    get_area_all,
    get_lockers_in_area,
    set_description,
    set_latitude,
    set_longitude,
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class AreaUnitTests(unittest.TestCase):
    def test_new_area(self):
        new_area = Area('A locker description',10.283759,-61.404937)
        assert new_area.longitude == 10.283759        
        assert new_area.latitude == -61.404937
        assert new_area.description == 'A locker description'

    def test_new_area_toJSON(self):
        new_area = Area('A locker description',10.259674,-61.411548)

        expected_json = {
            'id':None,
            'description':'A locker description',
            'longitude': 10.259674,
            'latitude': -61.411548
        }
        self.assertDictEqual(expected_json,new_area.toJSON())

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    os.unlink(os.getcwd()+"/App/py_test.db")
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    

class AreaIntegratedTests (unittest.TestCase):
    def test_add_new_area(self):
        new_area = add_new_area('A locker description',10.283759,-61.404937)
        #assert new_area.id == 1
        assert new_area.longitude == 10.283759        
        assert new_area.latitude == -61.404937
        assert new_area.description == 'A locker description'
    
    def test_get_area_by_id(self):
        area = get_area_by_id(1)
        assert area.id == 1
        assert area.longitude == 10.283759        
        assert area.latitude == -61.404937
        assert area.description == 'A locker description'

    def test_get_area_by_id_invalid(self):
        with pytest.raises(Exception) as E:
            area = get_area_by_id(0)
            self.assertIsNone(area)
    
    def test_set_description(self):
        area = set_description(1,'A new locker description')
        assert area.description == 'A new locker description'
    
    def test_set_description_invalid(self):
        with pytest.raises(Exception) as E:
            area = set_description(0,'A invalid locker description')
            self.assertIsNone(area)
    
    def test_set_latitude(self):
        area = set_latitude(1,9.47893)
        assert area.latitude == 9.47893
    
    def test_set_latitude_invalid(self):
        with pytest.raises(Exception) as E:
            area = set_latitude(0,9.47893)
            self.assertIsNone(area)

    def test_set_longitude(self):
        area = set_longitude(1,-99.40400)
        assert area.longitude == -99.40400

    def test_set_longitude_invalid(self):
        with pytest.raises(Exception) as E:
            area = set_longitude(0,-99.40400)
            self.assertIsNone(area)
    
    def test_delete_area(self):
        with pytest.raises(Exception) as E:
            add_new_area('A locker description',45.85739, -25.45543)
            area = delete_area(2)
            self.assertIsNotNone(area)
            self.assertIsNone(get_area_by_id(2))
    
    def test_delete_area_invalid(self):
        with pytest.raises(Exception) as E:
            area = delete_area(2)
            self.assertIsNone(area)
    
    def test_get_all_area(self):
        results =  get_area_all()
        expectedList = [{
            'id':1,
            'description':'A locker description',
            'longitude': 10.283759,
            'latitude': -61.404937
        }]
        self.assertListEqual(expectedList,results)
    
    def test_get_lockers_in_area(self):
        add_new_locker('AreaTestLocker','LARGE', 'FREE','TESTKEY1',1)
        add_new_locker('AreaTestLocker2','LARGE', 'FREE','TESTKEY2',1)
        lockers = get_lockers_in_area(1)
        expectedList = [{
            'locker_code':'AreaTestLocker',
            'locker_type':'Large',
            'status':'Free',
            'area':1
        },{
            'locker_code':'AreaTestLocker2',
            'locker_type':'Large',
            'status':'Free',
            'area':1
        }]
        self.assertListEqual(expectedList,lockers)
    
    def test_get_lockers_in_area_invalid(self):
        with pytest.raises(Exception) as E:
            lockers = get_lockers_in_area(999)
            lockers1 = get_lockers_in_area(None)
            lockers2 = get_lockers_in_area('1')
            self.assertIsNone(locker)
            self.assertIsNone(locker1)
            self.assertIsNone(locker2)