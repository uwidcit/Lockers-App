import os, pytest,logging,unittest
from App.main import create_app
from App.database import create_db
from App.models import MasterKey
from App.controllers import (
    new_masterkey,
    get_all_masterkeys,
    get_all_masterkeys_no_offset,
    get_masterkey_by_id,
    update_series,
    update_masterkey_id,
    delete_masterkey,
    update_masterkey_type,
    search_masterkey,
    get_key_masterkey_offset,
)
from datetime import datetime

from wsgi import app

LOGGER = logging.getLogger(__name__)

class MasterkeyUnitTests(unittest.TestCase):
    def test_create_new_masterkey(self):
        date = datetime(2023,1,31)
        new_m_key = MasterKey('TestMasterkey','MasterkeySeries','Lock',date.date())
        assert new_m_key.masterkey_id == "TestMasterkey"
        assert new_m_key.series == "MasterkeySeries"
        assert new_m_key.key_type.value == "Lock"
        assert new_m_key.date_added == date.date()

    def test_create_new_masterkey_toJSON(self):
        date = datetime(2023,1,31)
        new_m_key = MasterKey('TestMasterkey2','MasterkeySeries2','Combination',date)
        expected_json = {
            'masterkey_id':'TestMasterkey2',
            'series':'MasterkeySeries2',
            'key_type':'Combination',
            'date_added': datetime.strftime(date,'%Y-%m-%d')
        }
        self.assertDictEqual(expected_json,new_m_key.toJSON())


@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"/App/py_test.db")

class MasterkeyIntegratedTests(unittest.TestCase):
    def test_new_masterkey(self):
        date = datetime(2023,1,31)
        new_m_key = new_masterkey('TestMKey', 'TestSeries','LOCK', date)
        assert new_m_key.masterkey_id == "TestMKey"
        assert new_m_key.series == "TestSeries"
        assert new_m_key.key_type.value == "Lock"
        assert new_m_key.date_added == date.date()
    
    def test_get_all_masterkeys(self):
        date = datetime(2023,1,31)
        new_masterkey('Master1', 'M1','LOCK', date)
        new_masterkey('Master2', 'M2','Combination', date)
        new_masterkey('Master3', 'M3','LOCK', date)
        new_masterkey('Master4', 'M4','Combination', date)
        master_key_list = get_all_masterkeys(3,1)
        expected_json = {'num_pages':2, "data":[{
            'masterkey_id':'Master1',
            'series':'M1',
            'key_type':'Lock',
            'date_added': datetime.strftime(date,'%Y-%m-%d')
        }, {
            'masterkey_id':'Master2',
            'series':'M2',
            'key_type':'Combination',
            'date_added': datetime.strftime(date,'%Y-%m-%d')
        }, {
            'masterkey_id':'Master3',
            'series':'M3',
            'key_type':'Lock',
            'date_added': datetime.strftime(date,'%Y-%m-%d')
        }]}
        self.assertDictEqual(expected_json,master_key_list)

    def test_get_all_masterkeys_no_offset(self):
        date = datetime(2023,1,31)
        expected_list = ['Master1', 'Master2','Master3','Master4']
        master_key_list = get_all_masterkeys_no_offset()
        self.assertListEqual(expected_list,master_key_list)
    
    def test_get_masterkey_by_id(self):
        date = datetime(2023,1,31)
        masterkey = get_masterkey_by_id('Master1')
        assert masterkey.masterkey_id == "Master1"
        assert masterkey.series == "M1"
        assert masterkey.key_type.value == "Lock"
        assert masterkey.date_added == date.date()

    def test_get_masterkey_by_id_invalid(self):
        date = datetime(2023,1,31)
        masterkey = get_masterkey_by_id('')
        masterkey_2 = get_masterkey_by_id(None)
        masterkey_3 = get_masterkey_by_id('Invalid')
        self.assertIsNone(masterkey) 
        self.assertIsNone(masterkey_2)  
        self.assertIsNone(masterkey_3)
    
    def test_update_series(self):
        new_masterkey('Master5', 'z1','LOCK', datetime.now())
        masterkey = update_series('Master5','M5')
        assert masterkey.masterkey_id == 'Master5'
        assert masterkey.series == 'M5'

    def test_update_series_invalid(self):
        masterkey = update_series('','M5')
        masterkey2 = update_series(None,'Bubbles')
        masterkey3 = update_series('Master5',None)
        self.assertIsNone(masterkey)
        self.assertIsNone(masterkey2)
        self.assertIsNone(masterkey3)
       
    def test_update_masterkey_type(self):
        new_masterkey('Master6', 'M6','Combination', datetime.now())
        masterkey = update_masterkey_type('Master6','LOCK')
        assert masterkey.masterkey_id == 'Master6'
        assert masterkey.key_type.value == 'Lock'

    def test_update_masterkey_type_invalid(self):
        masterkey = update_masterkey_type('','LOCK')
        masterkey2 = update_masterkey_type('Master6',None)
        masterkey3 = update_masterkey_type(None,'')
        self.assertIsNone(masterkey) 
        self.assertIsNone(masterkey2)
        self.assertIsNone(masterkey3) 
    
    def test_search_masterkey(self):
        date = datetime(2023,1,31)
        query = search_masterkey('Combination',1,6)
        expected_json = {'num_pages':1, "data":[{
            'masterkey_id':'Master2',
            'series':'M2',
            'key_type':'Combination',
            'date_added': datetime.strftime(date,'%Y-%m-%d')
        },{
            'masterkey_id':'Master4',
            'series':'M4',
            'key_type':'Combination',
            'date_added': datetime.strftime(date,'%Y-%m-%d')
        }]}
        self.assertDictEqual(expected_json,query)
    
    
    



       