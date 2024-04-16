import os, pytest,logging,unittest
from App.main import create_app
from App.database import create_db
from App.models import Key
from App.controllers import (

)

from wsgi import app
LOGGER = logging.getLogger(__name__)

class KeyHistoryUnitTest(unittest.TestCase):
    def empty_test(self):
        return

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"/App/py_test.db")

class KeyHistoryIntegratedTest(unittest.TestCase):
    def empty_i_test(self):
        return