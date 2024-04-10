import os, pytest, logging, unittest
from App.database import create_db
from App.main import create_app
from App.models import RentTypes,Rent,TransactionLog
from App.controllers import (
    add_new_transaction,
    add_new_area,
    create_rent,
    init_amount_owed,
    get_rentType_by_id,
    get_rentType_by_period,
    add_new_locker,
    add_new_student,
    get_all_rentals,
    new_rentType,
    period_elapsed,
    recal_amount_owed,
    release_rental,
    add_new_area
)
from App.models.rent import RentStatus
from datetime import datetime,timedelta
from wsgi import app

LOGGER = logging.getLogger(__name__)

class RentTypeUnitTests(unittest.TestCase):
    def test_new_rent(self):
        date1 = datetime.now()
        date2 = timedelta(days = 30) + date1
        new_rent = Rent('816000000','1','1', date1, date2, 22.5, 'FIXED', None)
        assert new_rent.student_id == '816000000'
        assert new_rent.keyHistory_id == '1'
        assert new_rent.rent_date_from == date1
        assert new_rent.rent_date_to == date2
        assert new_rent.date_returned == None
        assert new_rent.amount_owed == 22.5
        assert new_rent.status.value == "Owed"

    def test_new_rent_overdue(self):
        new_rent = Rent('816001110','1','1', datetime(2022,2,15), datetime(2022,2,18),22.50, 'FIXED', None)
        assert new_rent.student_id == '816001110'
        assert new_rent.keyHistory_id == '1'
        assert new_rent.rent_date_from == datetime(2022,2,15)
        assert new_rent.rent_date_to == datetime(2022,2,18)
        assert new_rent.date_returned == None
        assert new_rent.amount_owed == 22.5
        assert new_rent.status.value == "Overdue"

    def test_new_rent_paid(self):
        new_rent = Rent('816000000','1','1', datetime(2023,2,15), datetime(2023,2,18),100, 'FIXED', None)
        new_rent.late_fees = 0
        new_rent.additional_fees = 0
        new_rent.update_payments(100)
        new_rent.status = new_rent.check_status()
        assert new_rent.student_id == '816000000'
        assert new_rent.keyHistory_id == '1'
        assert new_rent.rent_date_from == datetime(2023,2,15)
        assert new_rent.rent_date_to == datetime(2023,2,18)
        assert new_rent.date_returned == None
        assert new_rent.cal_amount_owed() == 0
        assert new_rent.status.value == "Paid"

    def test_new_rent_partial(self):
        new_rent = Rent('816000000','1','1', datetime(2023,2,15), datetime(2023,2,18),200, 'FIXED', None)
        new_rent.late_fees = 0
        new_rent.additional_fees = 0
        new_rent.update_payments(100)
        new_rent.status = new_rent.check_status()
        assert new_rent.student_id == '816000000'
        assert new_rent.keyHistory_id == '1'
        assert new_rent.rent_date_from == datetime(2023,2,15)
        assert new_rent.rent_date_to == datetime(2023,2,18)
        assert new_rent.date_returned == None
        assert new_rent.cal_amount_owed() == 100
        assert new_rent.status.value == "Partial"
    
    def test_new_rent_returned(self):
        new_rent = Rent('816001110','1','1', datetime(2022,2,15), datetime(2022,2,18),40, 'FIXED', datetime(2022, 2, 18))
        new_rent.late_fees = 0
        new_rent.additional_fees = 0
        new_rent.update_payments(40)
        new_rent.status = new_rent.check_status()
        assert new_rent.student_id == '816001110'
        assert new_rent.keyHistory_id == '1'
        assert new_rent.rent_date_from == datetime(2022,2,15)
        assert new_rent.rent_date_to == datetime(2022,2,18)
        assert new_rent.date_returned == datetime(2022, 2, 18)
        assert new_rent.cal_amount_owed() == 0
        assert new_rent.status.value == "Returned"
    
    def test_new_rent_toJSON(self):
        rent_date_from = datetime.now()
        rent_date_to = timedelta(days=30) + rent_date_from
        new_rent = Rent('816001110','1','1', rent_date_from, rent_date_to,22.50, 'FIXED', None)
        new_rent.late_fees = 0
        new_rent.additional_fees = 0
        expected_json = {
            'id': None,
            'student_id': '816001110',
            'keyHistory_id':'1', 
            'rent_type':'1',
            'rent_date_from':datetime.strftime(rent_date_from,'%Y-%m-%d %H:%M:%S'),
            'rent_date_to':datetime.strftime(rent_date_to,'%Y-%m-%d %H:%M:%S'),
            'rent_method': 'Period',
            'date_returned':'',
            'additional_fees': 0,
            'late_fees' : 0,
            'amount_owed':22.5,
            'status': 'Owed'
        } 
        self.assertDictEqual(expected_json,new_rent.toJSON())

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"/App/py_test.db")

class RentIntegratedTest(unittest.TestCase):
    def test_create_rent(self):
        area = add_new_area('ENG', 12, 20)
        add_new_student('816000111','Remmy','Dreamer','FST','18684981333','remmy.dreamer@my.uwi.edu')
        add_new_locker('A1001','MEDIUM','FREE','AVAILABLE',area.id)
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_type = get_rentType_by_period(period_from,period_to,'Daily')
        if rent_type is None:
            new_rentType(period_from,period_to,'Daily',4)
        rent_period_from = datetime.now()
        rent_period_from = rent_period_from.replace(hour = 8, minute = 0 ,second= 0, microsecond= 0)
        rent_period_to = rent_period_from + timedelta(days=5)
        rent = create_rent('816000111','A1001',1,rent_period_from,rent_period_to, 'RATE', None)
        assert rent.student_id == '816000111'
        assert rent.key_history.id == 1
        assert rent.rent_type == 1
        assert rent.rent_date_from == rent_period_from
        assert rent.rent_date_to == rent_period_to
        assert rent.date_returned is None
        assert rent.amount_owed == 20
        assert rent.status.value == 'Owed'
        assert rent.status.value == 'Owed'
    
    def test_period_elaspsed_daily(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_type = get_rentType_by_period(period_from,period_to,'Daily')
        if rent_type is None:
            rent_type =  new_rentType(period_from,period_to,'Daily',4)
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(18)
        time = period_elapsed(rent_type,rent_date_from,rent_date_to)
        assert time == 18

    def test_period_elaspsed_hourly(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_type = get_rentType_by_period(period_from,period_to,'Hourly')
        if rent_type is None:
            rent_type = new_rentType(period_from,period_to,'Hourly',2.50)
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(hours=5)
        time = period_elapsed(rent_type,rent_date_from,rent_date_to)
        assert time == 5
    
    def test_period_elaspsed_semester(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_type = get_rentType_by_period(period_from,period_to,'SEMESTERMEDIUM')
        if rent_type is None:
            rent_type = new_rentType(period_from,period_to,'SEMESTERMEDIUM',100)
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(days = 93)
        time = period_elapsed(rent_type,rent_date_from,rent_date_to)
        assert time == 1
    
    def test_q_init_amount_owed_daily(self):
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(days=3)
        amount = init_amount_owed(1,rent_date_from,rent_date_to)
        assert amount == 12
    
    def test_q_init_amount_owed_hourly(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_date_from = datetime.now()
        rent_type = get_rentType_by_period(period_from,period_to,'Hourly')
        if rent_type is None:
            rent_type = new_rentType(period_from,period_to,'Hourly',2.50)
        rent_date_to = rent_date_from + timedelta(hours=5)
        amount = init_amount_owed(rent_type.id,rent_date_from,rent_date_to)
        assert amount == 12.50

    def test_q_init_amount_owed_monthly(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_date_from = datetime.now()
        rent_date_to = rent_date_from + timedelta(days=31)
        rent_type = get_rentType_by_period(period_from,period_to,'DAILY')
        if rent_type is None:
            rent_type = new_rentType(period_from,period_to,'Daily',4)
        amount = init_amount_owed(rent_type.id,rent_date_from,rent_date_to)
        assert amount == 124
    
    def test_q_init_amount_owed_semester(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_date_from = datetime.now()
        rent_type = get_rentType_by_period(period_from,period_to,'SEMESTERMEDIUM')
        rent_date_to = rent_date_from + timedelta(days=90)
        if rent_type is None:
            rent_type = new_rentType(period_from,period_to,'SEMESTERMEDIUM',100)
        amount = init_amount_owed(rent_type.id,rent_date_from,rent_date_to)
        assert amount == 100
    
    def test_recal_amount_owed_daily(self):
        rent_date_from = datetime(2023,1,8)
        rent_date_to = rent_date_from + timedelta(days=2)
        date_returned = rent_date_to + timedelta(days=4)
        new_rent = Rent('816000000','1','1', rent_date_from, rent_date_to, 8, 'RATE', date_returned)
        new_rent = recal_amount_owed(new_rent,1,date_returned,rent_date_from,rent_date_to)
        assert new_rent.amount_owed == 8
        assert new_rent.late_fees == 16

    
    def test_recal_amount_owed_hourly(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_date_from = datetime(2023,1,8)
        rent_date_to = rent_date_from + timedelta(hours=2)
        date_returned = rent_date_to + timedelta(hours=480)
        
        rent_type = get_rentType_by_period(period_from,period_to,'Hourly')
        if rent_type is None:
            rent_type = new_rentType(period_from,period_to,'Hourly',2.50)
        new_rent = Rent('816000000','1','1', rent_date_from, rent_date_to, 5,'RATE' , date_returned)
        new_rent = recal_amount_owed(new_rent,rent_type.id,date_returned,rent_date_from,rent_date_to)
        assert new_rent.amount_owed == 5
        assert new_rent.late_fees == 1200
    
    def test_recal_amount_owed_weekly(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_date_from = datetime(2023,1,8)
        rent_date_to = rent_date_from + timedelta(days=3)
        date_returned = rent_date_to + timedelta(days=41)
        rent_type = get_rentType_by_period(period_from,period_to,'Daily')
        if rent_type is None:
            rent_type = new_rentType(period_from,period_to,'Daily',4)
        new_rent = Rent('816000000','1',rent_type.id, rent_date_from, rent_date_to, 12,'RATE' , date_returned)
        new_rent = recal_amount_owed(new_rent,rent_type.id,date_returned,rent_date_from,rent_date_to)
        assert new_rent.amount_owed == 12
        assert new_rent.late_fees == 164
    
    
    def test_recal_amount_owed_monthly_ontime(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_date_from = datetime(2023,1,8)
        rent_date_to = rent_date_from + timedelta(days=31)
        date_returned = rent_date_to + timedelta(days=375)
        rent_type = get_rentType_by_period(period_from,period_to,'Daily')
        if rent_type is None:
            rent_type = new_rentType(period_from,period_to,'Daily',4)
        new_rent = Rent('816000000','1',rent_type.id, rent_date_from, rent_date_to, 124,'RATE' , date_returned)
        new_rent = recal_amount_owed(new_rent,rent_type.id,date_returned,rent_date_from,rent_date_to)
        assert new_rent.amount_owed == 124
        assert new_rent.late_fees == 1500
    
    def test_recal_amount_owed_semester_ontime(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_date_from = datetime(2023,1,8)
        rent_date_to = rent_date_from + timedelta(days=93)
        date_returned = rent_date_to + timedelta(days=375)
        rent_type = get_rentType_by_period(period_from,period_to,'SEMESTERMEDIUM')
        if rent_type is None:
            rent_type = new_rentType(period_from,period_to,'SEMESTERMEDIUM',4)
        new_rent = Rent('816000000','1',rent_type.id, rent_date_from, rent_date_to, 100,'FIXED' , date_returned)
        new_rent = recal_amount_owed(new_rent,rent_type.id,date_returned,rent_date_from,rent_date_to)
        assert new_rent.amount_owed == 100
        assert new_rent.late_fees == 0
    
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
            'student_id': '816000111',
            'keyHistory_id':1,
            "additional_fees":0,
            'late_fees':0,
            'rent_type':1,
            'rent_method':'Rate',
            'rent_date_from':datetime.strftime(rent_period_from,'%Y-%m-%d %H:%M:%S'),
            'rent_date_to':datetime.strftime(rent_period_to,'%Y-%m-%d %H:%M:%S'),
            'date_returned':"",
            'amount_owed':20.0,
            'status':'Owed'
        }]
        actual_list = get_all_rentals()
        self.assertListEqual(expected_list,actual_list)