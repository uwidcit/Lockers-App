import os, pytest, logging, unittest,tempfile
from App.models import Student
from App.controllers import (
    add_new_student,
    get_student_by_id,
    get_student_by_id_json,
    get_all_students,
    update_student_first_name,
    update_student_last_name,
    update_student_phone_number,
    update_student_faculty
)
from App.main import create_app
from App.database import create_db,get_migrate
from wsgi import app

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
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"//py_test.db")


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
