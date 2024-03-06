import os, pytest, logging, unittest
from App.models import TransactionLog,Rent,RentTypes
from App.main import create_app
from App.database import create_db
from datetime import datetime
from App.controllers import (
    add_new_transaction,
    get_transaction_id,
    get_transaction_json,
    get_all_transactions,
    getT_Type
)
from wsgi import app

LOGGER = logging.getLogger(__name__)

class TransactionLogUnitTests(unittest.TestCase):
    def test_new_Transaction(self):
        date = datetime.now()
        new_trans = TransactionLog(1,'TTD',date,10.00,'Initial Deposit','Debit')
        assert new_trans.rent_id == 1
        assert new_trans.currency == 'TTD'
        assert new_trans.transaction_date == date
        assert new_trans.amount == 10.00
        assert new_trans.description == 'Initial Deposit'
        assert new_trans.type.value == 'debit'

    def test_new_Transaction_toJSON(self):
        date = datetime.now()
        new_trans = TransactionLog(2,'USD',date,40.00,'Overdue Payment','debit')

        expected_json ={
            'id': None,
            'rent_id':2,
            'currency':'USD',
            'transaction_date':date,
            'amount':40.00,
            'description':'Overdue Payment',
            'type': 'debit'
        }
        self.assertDictEqual(expected_json,new_trans.toJSON())

@pytest.fixture(autouse=True, scope="class")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"//py_test.db")

class TransactionLogIntegrationTest(unittest.TestCase):
    def test_add_transaction(self):
        date = datetime.now()
        transaction = add_new_transaction('1','TTD',date,'100', 'Downpayment','DEBIT')
        self.assertIsNotNone(transaction)
        new_trans = get_transaction_id(1)
        assert new_trans.rent_id == 1
        assert new_trans.currency == 'TTD'
        assert new_trans.transaction_date == date.date()
        assert new_trans.amount == 100.00
        assert new_trans.description == 'Downpayment'
        assert new_trans.type.value == 'debit'

    def test_get_Transaction_by_id_json(self):
        date = datetime.now()
        result = get_transaction_json(1)

        expected_json ={
            'id': 1,
            'rent_id':1,
            'currency':'TTD',
            'transaction_date':date.date(),
            'amount':100.00,
            'description':'Downpayment',
            'type': 'debit'
        }

        self.assertDictEqual(expected_json,result)
    
    def test_get_all_transactions(self):
        date = datetime.now()
        result = get_all_transactions()

        expected_list = [{
            'id': 1,
            'rent_id':1,
            'currency':'TTD',
            'transaction_date':date.date(),
            'amount':100.00,
            'description':'Downpayment',
            'type': 'debit'
        }]

        self.assertListEqual(expected_list,result)
    
    def test_get_TransactionType(self):
        expected_list = ['credit','debit']
        result = getT_Type()
        self.assertListEqual(expected_list,result)
    
