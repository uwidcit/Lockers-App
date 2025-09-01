import os, pytest, logging, unittest
from App.models import TransactionLog,Rent,RentTypes
from App.main import create_app
from App.database import create_db
from datetime import datetime, timedelta
from App.controllers import (
    add_new_transaction,
    get_transactions_by_offset,
    get_transaction_id,
    get_transaction_json,
    get_all_transactions,
    getT_Type,
    new_key,
    new_masterkey,
    add_new_area,
    add_new_locker,
    add_new_student,
    new_rentType,
    search_transaction,
    create_rent
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
            'type': 'debit',
            'receipt_number': None
        }
        self.assertDictEqual(expected_json,new_trans.toJSON())

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"/App/py_test.db")
    

class TransactionLogIntegrationTest(unittest.TestCase):
    def test_add_transaction(self): 
        date = datetime.now()
        masterkey = new_masterkey('test101','series','lock',date)
        key = new_key('k101','test101','Free',date)
        area = add_new_area('description', 10, 12)
        locker = add_new_locker('locker101','Small','Free','k101',area.id)
        student = add_new_student('816024666', 'Chris', 'Rock', 'FST','18681234567','chrisrock@myuwi.edu')
        rentType = new_rentType(date, timedelta(days = 2555) + date, 'SemesterSmall', 5)
        rent = create_rent('816024666', 'locker101',rentType.id, date, timedelta(weeks = 8) + date,'fixed',None)
        transaction = add_new_transaction(rent.id,'TTD',date,'100', 'Downpayment','DEBIT')
        print(transaction)
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
            'type': 'debit',
            'receipt_number': None
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
            'type': 'debit',
            'receipt_number': None
        }]

        self.assertListEqual(expected_list,result)
    
    def test_get_TransactionType(self):
        expected_list = ['credit','debit']
        result = getT_Type()
        self.assertListEqual(expected_list,result)
    
    def test_search_transaction(self):
        search_id = search_transaction(1,6,1)
        search_student = search_transaction('816024666',6,1)
        search_amount  = search_transaction(100,6,1)
        search_tType = search_transaction('debit', 6, 1)
        
        date = datetime.now()
        expected_list = [{
            'id': 1,
            'rent_id':1,
            'currency':'TTD',
            'transaction_date':date.date(),
            'amount':100.00,
            'description':'Downpayment',
            'type': 'debit',
            'receipt_number': None
        }]
        self.assertIsNotNone(search_id)
        self.assertIsNotNone(search_student)
        self.assertIsNotNone(search_amount)
        self.assertIsNotNone(search_tType)
        self.assertListEqual(expected_list,search_id['data'])
        self.assertListEqual(expected_list,search_student['data'])
        self.assertListEqual(expected_list,search_amount['data'])
        self.assertListEqual(expected_list,search_tType['data'])

    def test_get_transaction_by_offset(self):
        date = datetime.now()
        transactions = get_transactions_by_offset(6,1)
        expected_list = [{
            'id': 1,
            'rent_id':1,
            'currency':'TTD',
            'transaction_date':date.date(),
            'amount':100.00,
            'description':'Downpayment',
            'type': 'debit',
            'receipt_number': None
        }]
        self.assertListEqual(expected_list,transactions)

    
