import os, pytest, logging, unittest
from models import RentTypes,Rent,TransactionLog
from models.rent import Status
from datetime import datetime

LOGGER = logging.getLogger(__name__)

class RentTypeUnitTests(unittest.TestCase):
    def test_new_rent(self):
        new_rent = Rent('816000000','A1001','1', datetime(2023,2,15), datetime(2023,2,18),22.50)
        assert new_rent.student_id == '816000000'
        assert new_rent.locker_id == 'A1001'
        assert new_rent.rent_date_from == datetime(2023,2,15)
        assert new_rent.rent_date_to == datetime(2023,2,18)
        assert new_rent.date_returned == None
        assert new_rent.amount_owed == 22.5
        assert new_rent.status.value == "Owed"

    def test_new_rent_overdue(self):
        new_rent = Rent('816001110','A1111','1', datetime(2022,2,15), datetime(2022,2,18),22.50)
        assert new_rent.student_id == '816001110'
        assert new_rent.locker_id == 'A1111'
        assert new_rent.rent_date_from == datetime(2022,2,15)
        assert new_rent.rent_date_to == datetime(2022,2,18)
        assert new_rent.date_returned == None
        assert new_rent.amount_owed == 22.5
        assert new_rent.status.value == "Overdue"

    def test_new_rent_paid(self):
        new_rent = Rent('816000000','A1001','1', datetime(2023,2,15), datetime(2023,2,18),0)
        new_rent.Transactions = [TransactionLog(None,'TTD',datetime(2023,1,1),15,'Description','Debit'),TransactionLog(None,'TTD',datetime(2023,1,5),15,'Description','Debit')]
        new_rent.status = new_rent.check_status()
        assert new_rent.student_id == '816000000'
        assert new_rent.locker_id == 'A1001'
        assert new_rent.rent_date_from == datetime(2023,2,15)
        assert new_rent.rent_date_to == datetime(2023,2,18)
        assert new_rent.date_returned == None
        assert new_rent.amount_owed == 0
        assert new_rent.status.value == "Paid"

    def test_new_rent_partial(self):
        new_rent = Rent('816000000','A1001','1', datetime(2023,2,15), datetime(2023,2,18),200)
        new_rent.Transactions = [TransactionLog(None,'TTD',datetime(2023,1,1),15,'Description','Debit'),TransactionLog(None,'TTD',datetime(2023,1,5),15,'Description','Debit')]
        new_rent.status = new_rent.check_status()
        assert new_rent.student_id == '816000000'
        assert new_rent.locker_id == 'A1001'
        assert new_rent.rent_date_from == datetime(2023,2,15)
        assert new_rent.rent_date_to == datetime(2023,2,18)
        assert new_rent.date_returned == None
        assert new_rent.amount_owed == 200
        assert new_rent.status.value == "Partial"
    
    def test_new_rent_returned(self):
        new_rent = Rent('816001110','A1111','1', datetime(2022,2,15), datetime(2022,2,18),0)
        new_rent.status = Status.RETURNED
        assert new_rent.student_id == '816001110'
        assert new_rent.locker_id == 'A1111'
        assert new_rent.rent_date_from == datetime(2022,2,15)
        assert new_rent.rent_date_to == datetime(2022,2,18)
        assert new_rent.date_returned == None
        assert new_rent.amount_owed == 0
        assert new_rent.status.value == "Returned"
    
    def test_new_rent_toJSON(self):
        new_rent = Rent('816001110','A1111','1', datetime(2023,2,15), datetime(2023,2,18),22.50)
        expected_json = {
            'id': None,
            'student_id': '816001110',
            'locker_id':'A1111',
            'rent_type':'1',
            'rent_date_from':datetime(2023,2,15),
            'rent_date_to':datetime(2023,2,18),
            'date_returned':None,
            'amount_owed':22.5,
            'status':Status.OWED
        } 
        self.assertDictEqual(expected_json,new_rent.toJSON())

