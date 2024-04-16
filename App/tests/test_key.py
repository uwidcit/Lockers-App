import os, pytest,logging,unittest
from App.main import create_app
from App.database import create_db
from App.models import MasterKey, Key
from App.controllers import (
    get_all_keys
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
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"/App/py_test.db")

class KeyIntegratedTests(unittest.TestCase):
    def empty_i_test(self):
        assert None