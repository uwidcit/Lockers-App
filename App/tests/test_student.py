import os, pytest, logging, unittest,tempfile
from App.models import Student
from App.controllers import (
    add_new_student,
    add_new_area,
    add_new_locker,
    new_rentType,
    create_rent,
    get_available_student,
    get_student_by_id,
    get_students_by_offset,
    get_student_by_id_json,
    get_student_current_rental,
    get_rental_student,
    get_all_students,
    search_student,
    update_student_first_name,
    update_student_email,
    update_student_last_name,
    update_student_phone_number,
    update_student_status,
    update_student_faculty
)
from App.main import create_app
from App.database import create_db,get_migrate
from wsgi import app
from datetime import datetime,timedelta

LOGGER = logging.getLogger(__name__)

class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        new_student = Student('816000000','Test','Student','FSS','18684993333','test.student@my.uwi.edu')
        assert new_student.student_id == '816000000'
        assert new_student.first_name == 'Test'
        assert new_student.last_name == 'Student'
        assert new_student.faculty == 'FSS'
        assert new_student.phone_number == '18684993333'
        assert new_student.email == 'test.student@my.uwi.edu'

    def test_new_student_toJSON(self):
         new_student = Student('816000111','Remmy','Dreamer','FST','18684981333','remmy.dreamer@my.uwi.edu')
         expected_json = {
            'student_id':'816000111',
            'first_name':'Remmy',
            'last_name': 'Dreamer',
            'faculty':'FST',
            'phone_number':'18684981333',
            'email': 'remmy.dreamer@my.uwi.edu',
            'rentStanding' :'GOOD'
        }

         self.assertDictEqual(expected_json,new_student.toJSON())

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    os.unlink(os.getcwd()+"/App/py_test.db")
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    


class StudentIntegrationTest(unittest.TestCase):
    def test_add_student(self):
        add_new_student('816000111','Remmy','Dreamer','FST','18684981333','remmy.dreamer@my.uwi.edu')
        result = get_student_by_id('816000111')
        assert result.student_id == '816000111'
        assert result.first_name == 'Remmy'
        assert result.last_name == 'Dreamer'
        assert result.faculty == 'FST'
        assert result.phone_number == '18684981333'
        assert result.email == 'remmy.dreamer@my.uwi.edu'

    def test_get_student_by_id_json(self):
        add_new_student('816000111','Remmy','Dreamer','FST','18684981333','remmy.dreamer@my.uwi.edu')
        result = get_student_by_id_json('816000111')
        expected_json = {
            'student_id':'816000111',
            'first_name':'Remmy',
            'last_name': 'Dreamer',
            'faculty':'FST',
            'phone_number':'18684981333',
            'email': 'remmy.dreamer@my.uwi.edu',
            'rentStanding' :'GOOD'
        }
        self.assertDictEqual(expected_json,result)
    
    def test_get_student_by_id_json_invalid(self):
        result = get_student_by_id_json('816000000')
        self.assertIsNone(None,result)

    def test_update_student_fName(self):
         add_new_student('816000111','Remmy','Dreamer','FST','18684981333','remmy.dreamer@my.uwi.edu')
         update_student_first_name('816000111', 'Rem')
         result = get_student_by_id(816000111)
         assert result.first_name == "Rem" 
    
    def test_update_student_fName_invalid(self):
         result = update_student_first_name('816000111', 'Rem')
         self.assertIsNone(result)

    def test_update_student_lName(self):
         add_new_student('816000111','Remmy','Dreamer','FST','18684981333','remmy.dreamer@my.uwi.edu')
         update_student_last_name('816000111', 'Sleeper')
         result = get_student_by_id('816000111')
         assert result.last_name == "Sleeper" 

    def test_update_student_lName_invalid(self):
         result = update_student_last_name('81600000', 'Sleeper')
         self.assertIsNone (result)

    def test_update_student_phone_number(self):
         add_new_student('816000111','Remmy','Dreamer','FST','18684981333','remmy.dreamer@my.uwi.edu')
         update_student_phone_number('816000111', 18681112222)
         result = get_student_by_id('816000111')
         assert result.phone_number == '18681112222'

    def test_update_student_phone_number_invalid(self):
         result = update_student_phone_number('81600000', 18991112222)
         self.assertIsNone (result)

    def test_update_student_faculty(self):
         add_new_student('816000111','Remmy','Dreamer','FST','18684981333','remmy.dreamer@my.uwi.edu')
         update_student_faculty('816000111', 'ENG')
         result = get_student_by_id('816000111')
         assert result.faculty == 'ENG'

    def test_update_student_lName_invalid(self):
         result = update_student_faculty('81600000', 'ENG')
         self.assertIsNone (result)
    
    def test_update_student_email(self):
        add_new_student('812345678','Test','Student','AAA','18680001111','falseemail@my.uwi.edu')
        student = update_student_email('812345678','test.student@my.uwi.edu')
        assert student.student_id == '812345678'
        assert student.email == 'test.student@my.uwi.edu'
    
    def test_update_student_status(self):
        student = add_new_student('0101010','Space','Time','AAA','18681111111','spacetime@my.uwi.edu')
        assert student.rentStanding.value == "GOOD"
        student = update_student_status('0101010','Renting')
        assert student.rentStanding.value == "RENTING"
        student = update_student_status('0101010','Overdue')
        assert student.rentStanding.value == "OVERDUE"
        student = update_student_status('0101010','Owed')
        assert student.rentStanding.value == "OWED"

        
    def test_get_all_students(self):
        result = get_all_students()
        expected_list = [{
            'student_id':'816000111',
            'first_name':'Remmy',
            'last_name': 'Dreamer',
            'faculty':'FST',
            'phone_number':'18684981333',
            'email': 'remmy.dreamer@my.uwi.edu',
            'rentStanding' :'GOOD'
        }]
        self.assertListEqual(expected_list,result)
    
    def test_get_available_student(self):
        add_new_student('00001111','Emmy','Style','AAA','18689998888','emmy.style@my.uwi.edu')
        add_new_student('22221111','George','Style','AAA','18689998888','gstyle@my.uwi.edu')
        update_student_status('00001111','Overdue')
        update_student_status('22221111','RENTING')
        students = get_available_student(6,1)
        expected_json = {'num_pages':1, 'data':[{
            'student_id':'816000111',
            'first_name':'Remmy',
            'last_name': 'Dreamer',
            'faculty':'FST',
            'phone_number':'18684981333',
            'email': 'remmy.dreamer@my.uwi.edu',
            'rentStanding' :'GOOD'
        },{
            'student_id':'22221111',
            'first_name':'George',
            'last_name': 'Style',
            'faculty':'AAA',
            'phone_number':'18689998888',
            'email': 'gstyle@my.uwi.edu',
            'rentStanding' :'RENTING'
        }]}
        self.assertDictEqual(expected_json,students)

    def test_get_students_by_offset(self):
        students = get_students_by_offset(2,1)
        expected_json = {'num_pages':4, 'data':[{
            'student_id':'816000111',
            'first_name':'Remmy',
            'last_name': 'Dreamer',
            'faculty':'FST',
            'phone_number':'18684981333',
            'email': 'remmy.dreamer@my.uwi.edu',
            'rentStanding' :'GOOD'
        },{
            'student_id':'00001111',
            'first_name':'Emmy',
            'last_name': 'Style',
            'faculty':'AAA',
            'phone_number':'18689998888',
            'email': 'emmy.style@my.uwi.edu',
            'rentStanding' :'OVERDUE'
        }]}
        self.assertDictEqual(expected_json,students)

    def test_search_student(self):
        search_f_name = search_student('Emmy',1,2)
        search_l_name =search_student('Style',2,1)
        search_id = search_student('816000111',3,1)
        search_faculty = search_student('AAA',3,1)
        search_email = search_student('@my.uwi.edu',3,1)
        search_phone = search_student('18689998888',3,1)
        search_rent_standing = search_student('GOOD',1,1)

        expected_json1 = {'num_pages':2, 'data':[{
            'student_id':'00001111',
            'first_name':'Emmy',
            'last_name': 'Style',
            'faculty':'AAA',
            'phone_number':'18689998888',
            'email': 'emmy.style@my.uwi.edu',
            'rentStanding' :'OVERDUE'
        }]}
        expected_json2 = {'num_pages':1, 'data':[{
            'student_id':'00001111',
            'first_name':'Emmy',
            'last_name': 'Style',
            'faculty':'AAA',
            'phone_number':'18689998888',
            'email': 'emmy.style@my.uwi.edu',
            'rentStanding' :'OVERDUE'
        },{
            'student_id':'22221111',
            'first_name':'George',
            'last_name': 'Style',
            'faculty':'AAA',
            'phone_number':'18689998888',
            'email': 'gstyle@my.uwi.edu',
            'rentStanding' :'RENTING'
        }]} 

        expected_json3 = {'num_pages':1, 'data':[{
            'student_id':'816000111',
            'first_name':'Remmy',
            'last_name': 'Dreamer',
            'faculty':'FST',
            'phone_number':'18684981333',
            'email': 'remmy.dreamer@my.uwi.edu',
            'rentStanding' :'GOOD'
        }]}

        expected_json4 =  {'num_pages':1, 'data':[{
            'student_id':'816000111',
            'first_name':'Remmy',
            'last_name': 'Dreamer',
            'faculty':'FST',
            'phone_number':'18684981333',
            'email': 'remmy.dreamer@my.uwi.edu',
            'rentStanding' :'GOOD'
        },{
            'student_id':'00001111',
            'first_name':'Emmy',
            'last_name': 'Style',
            'faculty':'AAA',
            'phone_number':'18689998888',
            'email': 'emmy.style@my.uwi.edu',
            'rentStanding' :'OVERDUE'
        },{
            'student_id':'22221111',
            'first_name':'George',
            'last_name': 'Style',
            'faculty':'AAA',
            'phone_number':'18689998888',
            'email': 'gstyle@my.uwi.edu',
            'rentStanding' :'RENTING'
        }]}

        self.assertDictEqual(expected_json1, search_f_name)
        self.assertDictEqual(expected_json2, search_l_name)
        self.assertDictEqual(expected_json3, search_id)
        self.assertDictEqual(expected_json2, search_faculty)
        self.assertDictEqual(expected_json2, search_phone)
        self.assertDictEqual(expected_json4, search_email)
        self.assertDictEqual(expected_json3, search_rent_standing)

    def test_get_current_rental_student(self):
        area = add_new_area('ENG', 12, 20)
        add_new_student('845454545','Test','StudentRent','FSS','18005882300','test.StudenntRent@my.gmail.edu')
        add_new_locker('A1001','MEDIUM','FREE','AVAILABLE',area.id)
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_type = new_rentType(period_from,period_to,'Daily',4)
        rent_period_from = datetime.now()
        rent_period_from = rent_period_from.replace(hour = 8, minute = 0 ,second= 0, microsecond= 0)
        rent_period_to = rent_period_from + timedelta(days=5)
        create_rent('845454545','A1001',1,rent_period_from,rent_period_to, 'RATE', None)
        rental = get_student_current_rental('845454545')
        expected_json = {
            'id': 1,
            'student_id': '845454545',
            'keyHistory_id':1, 
            'rent_type':1,
            'rent_date_from':datetime.strftime(rent_period_from,'%Y-%m-%d %H:%M:%S'),
            'rent_date_to':datetime.strftime(rent_period_to,'%Y-%m-%d %H:%M:%S'),
            'rent_method': 'Rate',
            'date_returned':'',
            'additional_fees': 0.0,
            'late_fees' : 0.0,
            'amount_owed':20.00,
            'status': 'Owed'
        } 
        self.assertDictEqual(expected_json,rental)
    
    def test_get_rental_student(self):
        rent_period_from = datetime.now()
        rent_period_from = rent_period_from.replace(hour = 8, minute = 0 ,second= 0, microsecond= 0)
        rent_period_to = rent_period_from + timedelta(days=5)
        rental = get_rental_student('845454545',6,1)
        expected_json = {'num_pages':1, 'data':[{ 'id': 1,
            'student_id': '845454545',
            'keyHistory_id':1, 
            'rent_type':1,
            'rent_date_from':datetime.strftime(rent_period_from,'%Y-%m-%d %H:%M:%S'),
            'rent_date_to':datetime.strftime(rent_period_to,'%Y-%m-%d %H:%M:%S'),
            'rent_method': 'Rate',
            'date_returned':'',
            'additional_fees': 0.0,
            'late_fees' : 0.0,
            'amount_owed':20.00,
            'status': 'Owed'}]
        } 
        self.assertDictEqual(expected_json,rental)
