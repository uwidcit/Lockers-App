import os, pytest,logging,unittest
from App.main import create_app
from App.database import create_db
from App.models import Key
from App.controllers import (
    delete_key,
    get_all_keys,
    get_all_keys_id,
    get_key_by_id,
    get_key_statuses,
    new_key,
    new_masterkey,
    update_key_masterkey_id,
    update_key_status,
    
)

from wsgi import app
from datetime import datetime
LOGGER = logging.getLogger(__name__)

class KeyUnitTests(unittest.TestCase):
    def test_create_key(self):
        date = datetime.now()
        key = Key('TestKey', 'Master1','AVAILABLE',date.date())
        assert key.key_id == 'TestKey'
        assert key.masterkey_id == 'Master1'
        assert key.key_status.value == 'Available'
        assert key.date_added == date.date()

    def test_create_key_toJSON(self):
        date = datetime.now()
        key = Key('TestKey3', 'Master3','Lost',date.date())
        expected_json = {
            'key_id':'TestKey3',
            'masterkey_id':'Master3',
            'key_status':'Lost',
            'date_added': datetime.strftime(date,'%Y-%m-%d'),
            'KeyHistory': None,
        }
        self.assertDictEqual(expected_json,key.toJSON())


@pytest.fixture(autouse=True, scope="module")
def empty_db():
    os.unlink(os.getcwd()+"/App/py_test.db")
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    

class KeyIntegratedTests(unittest.TestCase):
    def test_new_key(self):
        date = datetime.now()
        new_masterkey('TestMasterKey1', 'Series', 'LOCK',date)
        key = new_key('TestKey1', 'TestMasterKey1','AVAILABLE',date)
        assert key.key_id == 'TestKey1'
        assert key.masterkey_id == 'TestMasterKey1'
        assert key.key_status.value == 'Available'
        assert key.date_added == date.date()
    
    def test_get_all_keys(self):
        date = datetime.now().date()
        new_masterkey('TestMasterKey2', 'Series', 'COMBINATION',date)
        new_key('TestKey2', 'TestMasterKey2','AVAILABLE',date)
        new_key('TestKey21', 'TestMasterKey2','AVAILABLE',date)
        keys = get_all_keys(6,1)
        expected_json ={
            "num_pages":1,
            "data": [{
            'key_id':'TestKey2',
            'masterkey_id':'TestMasterKey2',
            'key_status':'Available',
            'date_added': datetime.strftime(date,'%Y-%m-%d'),
            'KeyHistory': None,
        },{
            'key_id':'TestKey21',
            'masterkey_id':'TestMasterKey2',
            'key_status':'Available',
            'date_added': datetime.strftime(date,'%Y-%m-%d'),
            'KeyHistory': None,
        }]}
        self.assertDictEqual(expected_json,keys)

    def test_get_key_by_id(self):
        date = datetime.now()
        key = get_key_by_id('TestKey2')
        self.assertIsNotNone(key)
        assert key.key_id == 'TestKey2'
        assert key.masterkey_id == 'TestMasterKey2'
        assert key.key_status.value == 'Available'
        assert key.date_added == date.date()

    def test_get_key_by_id_invalid(self):
        key = get_key_by_id('InvalidKey')
        key2 = get_key_by_id('')
        key3 = get_key_by_id(None)
        self.assertIsNone(key)
        self.assertIsNone(key2)
        self.assertIsNone(key3)
    
    def test_update_key_masterkey_id(self):
        date = datetime.now()
        key = update_key_masterkey_id('TestKey21','TestMasterKey1')
        self.assertIsNotNone(key)
        assert key.key_id == 'TestKey21'
        assert key.masterkey_id == 'TestMasterKey1'
        assert key.key_status.value == 'Available'
        assert key.date_added == date.date()
    
    def test_update_key_masterkey_id_invalid(self):
        key = update_key_masterkey_id('InvalidKey','TestMasterKey1')
        key2 = update_key_masterkey_id('TestKey21','InvalidMKey')
        key3 = update_key_masterkey_id(None,None)
        key4 = update_key_masterkey_id('','')
        self.assertIsNone(key)
        self.assertIsNone(key2)
        self.assertIsNone(key3)
        self.assertIsNone(key4)

    def test_update_key_status(self):
        date = datetime.now()
        new_key('TestKey47', 'TestMasterKey2','LOST',date)
        key = update_key_status('TestKey47','Cutting')
        self.assertIsNotNone(key)
        assert key.key_id == 'TestKey47'
        assert key.masterkey_id == 'TestMasterKey2'
        assert key.key_status.value == 'Cutting'
        assert key.date_added == date.date()
    
    def test_update_key_status_invalid(self):
        key = update_key_status('TestKey47','InvalidStatus')
        key2 = update_key_status('InvalidKey','Cutting')
        key3 = update_key_status('','')
        key4 = update_key_status('TestKey47',None)
        self.assertIsNone(key)
        self.assertIsNone(key2)
        self.assertIsNone(key3)
        self.assertIsNone(key4)
        

    def test_delete_key(self):
        date = datetime.now().date()
        new_key('DeleteKey', 'TestMasterKey2','LOST',date)
        self.assertIsNotNone(delete_key("DeleteKey"))
        self.assertIsNone(get_key_by_id('DeleteKey'))

    def test_delete_key_invalid(self):
        self.assertIsNone(delete_key("DeleteKeyInvalid"))
    
    def test_get_key_statuses(self):
        expected_list= ['Available', 'Unavailable','Lost','Cutting','Ready']
        key_statuses = get_key_statuses()
        self.assertListEqual(expected_list,key_statuses)

    def test_get_all_keys_id(self):
        keys = get_all_keys_id()
        expected_list = ['TestKey2','TestKey21']
        self.assertListEqual(expected_list,keys)
        


