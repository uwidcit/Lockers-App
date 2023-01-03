import os, pytest, logging, unittest
from models import Student

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