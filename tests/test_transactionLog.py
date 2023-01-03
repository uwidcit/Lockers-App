import os, pytest, logging, unittest
from models import TransactionLog,Rent,RentTypes
from datetime import datetime

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
