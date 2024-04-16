import os, pytest,logging,unittest
from App.main import create_app
from datetime import datetime
from App.database import create_db
from App.models import KeyHistory
from App.controllers import (
    new_keyHistory,
    restore_keyHistory,
    deactivate,
    getKeyHistory,
    getKeyHistory_by_id,
    changeDateMove,
    getKeyHistory_all
)

from wsgi import app
LOGGER = logging.getLogger(__name__)

class KeyHistoryUnitTest(unittest.TestCase):
    def empty_test(self):
        return

    def test_KeyHistory(self):
        date = datetime.now()
        key_history = KeyHistory('K101', 'A101', date, 'Active')
        assert key_history.key_id == 'K101'
        assert key_history.locker_id == 'A101'
        assert key_history.date_moved == date

    def test_keyHistory_toJSON(self):
        date = datetime.now()
        key_history = KeyHistory('K101','A101', date, 'Active')
        expected_json = {
            'id': None,
            'key_id':'K101',
            'locker_id':'A101',
            'date_moved': date
        }
        self.assertDictEqual(expected_json,key_history.toJSON())

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"/App/py_test.db")

class KeyHistoryIntegratedTest(unittest.TestCase):
    def empty_i_test(self):
        return

    def test_new_keyHistory(self):
        date = datetime.now().date()
        newkeyH = new_keyHistory('K101','A101',date)
        assert newkeyH.key_id == 'K101'
        assert newkeyH.locker_id == 'A101'
        assert newkeyH.date_moved == date

    def test_deactivate(self):
        date = datetime.now().date()
        newkeyH = new_keyHistory('K101','A101',date)
        deactivate_key = deactivate(newkeyH.id)
        assert deactivate_key.id == newkeyH.id
        assert deactivate_key.key_id == 'K101'
        assert deactivate_key.locker_id == 'A101'
        assert deactivate_key.date_moved == date
        assert deactivate_key.isActive.value == 'Inactive'

    def test_getKeyHistory(self):
        date = datetime.now().date()
        newkeyH = new_keyHistory('K105','A105',date)
        getkeyH = getKeyHistory(newkeyH.id)
        assert getkeyH.id == newkeyH.id
        assert getkeyH.key_id == 'K105'
        assert getkeyH.locker_id == 'A105'
        assert getkeyH.date_moved == date
        assert getkeyH.isActive.value == 'Active'

    def test_getKeyHistory_by_id(self):
        expected_json ={'num_pages':1, "data":[{
            'id': 1,
            'key_id':'K101',
            'locker_id':'A101',
            'date_moved': datetime.now().date()
        }]}
        getkeyH_id = getKeyHistory_by_id('K101',6,1)
        self.assertDictEqual(expected_json, getkeyH_id)