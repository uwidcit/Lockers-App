import os, pytest, logging, unittest
from App.database import create_db
from App.main import create_app
from App.models import RentTypes,Rent,TransactionLog
from App.controllers import (
    add_new_transaction,
    create_rent,
    init_amount_owed,
    add_new_locker,
    add_new_student,
    get_all_rentals,
    new_rentType,
    period_elapsed,
    recal_amount_owed,
    release_rental
)
from App.models.rent import RentStatus
from datetime import datetime,timedelta
from wsgi import app

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

@pytest.fixture(autouse=True, scope="class")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"/App/py_test.db")

class RentIntegratedTest(unittest.TestCase):
    def test_create_rent(self):
        add_new_student('816000111','Remmy','Dreamer','FST','18684981333','remmy.dreamer@my.uwi.edu')
        add_new_locker('A1001','MEDIUM','FREE','AVAILABLE')

        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        new_rentType(period_from,period_to,'Daily',4)

        rent_period_from = datetime.now()
        rent_period_from = rent_period_from.replace(hour = 8, minute = 0 ,second= 0, microsecond= 0)
        rent_period_to = rent_period_from + timedelta(days=5)
        rent = create_rent('816000111','A1001',1,rent_period_from,rent_period_to)
        assert rent.student_id == 816000111
        assert rent.locker_id == 'A1001'
        assert rent.rent_type == 1
        assert rent.rent_date_from == rent_period_from
        assert rent.rent_date_to == rent_period_to
        assert rent.date_returned is None
        assert rent.amount_owed == 20
        assert rent.status == Status.OWED
    
    def test_period_elaspsed_daily(self):
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(18)
        time = period_elapsed(1,rent_date_from,rent_date_to)
        assert time == 18

    def test_period_elaspsed_hourly(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        new_rentType(period_from,period_to,'Hourly',2.50)
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(hours=5)
        time = period_elapsed(2,rent_date_from,rent_date_to)
        assert time == 5
    
    def test_period_elaspsed_t_weekly(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        new_rentType(period_from,period_to,'Weekly',8)
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(days = 21)
        time = period_elapsed(5,rent_date_from,rent_date_to)
        assert time == 3

    def test_period_elaspsed_monthly(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        new_rentType(period_from,period_to,'Monthly',30)
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(days = 31)
        time = period_elapsed(3,rent_date_from,rent_date_to)
        assert time == 1
    
    def test_period_elaspsed_semester(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        new_rentType(period_from,period_to,'Semester',100)
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(days = 93)
        time = period_elapsed(4,rent_date_from,rent_date_to)
        assert time == 1
    
    def test_q_init_amount_owed_daily(self):
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(days=3)
        amount = init_amount_owed(1,rent_date_from,rent_date_to)
        assert amount == 12
    
    def test_q_init_amount_owed_hourly(self):
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(hours=5)
        amount = init_amount_owed(2,rent_date_from,rent_date_to)
        assert amount == 12.50

    def test_q_init_amount_owed_monthly(self):
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(days=62)
        amount = init_amount_owed(3,rent_date_from,rent_date_to)
        assert amount == 60
    
    def test_q_init_amount_owed_semester(self):
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(days=93)
        amount = init_amount_owed(4,rent_date_from,rent_date_to)
        assert amount == 100
    
    def test_recal_amount_owed_daily_ontime(self):
        rent_date_from = datetime(2023,1,8)
        rent_date_to = rent_date_from + timedelta(days=2)
        date_returned = datetime.now()
        amt = recal_amount_owed(1,date_returned,rent_date_from,rent_date_to)
        assert amt == 8
    
    def test_recal_amount_owed_daily_late(self):
        rent_date_from = datetime(2023,1,2)
        rent_date_to = rent_date_from + timedelta(days=2)
        date_returned = datetime.now()
        amt = recal_amount_owed(1,date_returned,rent_date_from,rent_date_to)
        assert amt == 32
    
    def test_recal_amount_owed_hourly_ontime(self):
        rent_date_from = datetime(2023,1,8,7,30,0)
        rent_date_to = rent_date_from + timedelta(hours=5)
        date_returned = rent_date_to
        amt = recal_amount_owed(2,date_returned,rent_date_from,rent_date_to)
        assert amt == 12.50
    
    def test_recal_amount_owed_hourly_late(self):
        rent_date_from = datetime(2023,1,2,8,0,0)
        rent_date_to = rent_date_from + timedelta(hours=2)
        date_returned = rent_date_to + timedelta(hours=4)
        amt = recal_amount_owed(2,date_returned,rent_date_from,rent_date_to)
        assert amt == 15
    
    def test_recal_amount_owed_weekly_ontime(self):
        rent_date_from = datetime(2023,1,8)
        rent_date_to = rent_date_from + timedelta(days=7)
        date_returned = rent_date_to
        amt = recal_amount_owed(5,date_returned,rent_date_from,rent_date_to)
        assert amt == 8
    
    def test_recal_amount_owed_weekly_late(self):
        rent_date_from = datetime(2023,1,2)
        rent_date_to = rent_date_from + timedelta(days=21)
        date_returned = rent_date_to + timedelta(days=3)
        amt = recal_amount_owed(5,date_returned,rent_date_from,rent_date_to)
        assert amt == 36
    
    def test_recal_amount_owed_monthly_ontime(self):
        rent_date_from = datetime(2023,1,8)
        rent_date_to = rent_date_from + timedelta(days=31)
        date_returned = datetime.now()
        amt = recal_amount_owed(3,date_returned,rent_date_from,rent_date_to)
        assert amt == 30
    
    def test_recal_amount_owed_monthly_late(self):
        rent_date_from = datetime(2023,1,2)
        rent_date_to = rent_date_from + timedelta(days=30)
        date_returned = rent_date_to + timedelta(days=10)
        amt = recal_amount_owed(3,date_returned,rent_date_from,rent_date_to)
        assert amt == 70
    
    def test_recal_amount_owed_semester_ontime(self):
        rent_date_from = datetime(2023,1,8)
        rent_date_to = rent_date_from + timedelta(days=93)
        date_returned = rent_date_to
        amt = recal_amount_owed(4,date_returned,rent_date_from,rent_date_to)
        assert amt == 100
    
    def test_recal_amount_owed_semester_late(self):
        rent_date_from = datetime(2023,1,2)
        rent_date_to = rent_date_from + timedelta(days=93)
        date_returned = rent_date_to + timedelta(days = 15)
        amt = recal_amount_owed(4,date_returned,rent_date_from,rent_date_to)
        assert amt == 160
    
    def release_rental(self):
        add_new_student('816000222','Test','Student','ENG','18684998888','test.student@my.uwi.edu')
        add_new_locker('A1231','Small','FREE','AVAILABLE')
        rent_period_from = datetime.now()
        rent_period_from = rent_period_from.replace(hour = 8, minute = 0 ,second= 0, microsecond= 0)
        rent_period_to = rent_period_from + timedelta(days=2)
        add_new_transaction(2,'TTD',rent_period_to,4,'Payment','Debit')
        create_rent('816000111','A1231',1,rent_period_from,rent_period_to)
        rent = release_rental(2,rent_period_to)
        self.assertIsNotNone(rent)
        assert rent.status == Status.RETURNED

    def test_get_all_rentals(self):
        rent_period_from = datetime.now()
        rent_period_from  = rent_period_from.replace(hour = 8, minute = 0 ,second= 0, microsecond= 0)
        rent_period_to = rent_period_from + timedelta(days=5)
        expected_list = [{
            'id': 1,
            'student_id': 816000111,
            'locker_id':'A1001',
            'rent_type':1,
            'rent_date_from':rent_period_from,
            'rent_date_to':rent_period_to,
            'date_returned':None,
            'amount_owed':20.0,
            'status':Status.OWED
        }]
        actual_list = get_all_rentals()
        self.assertListEqual(expected_list,actual_list)