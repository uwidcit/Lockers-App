import os, pytest,logging,unittest
from App.main import create_app
from App.database import create_db
from App.models import Notes
from App.controllers import (
    create_comment,
    add_new_area,
    add_new_locker,
    add_new_student,
    create_rent,
    get_comment,
    get_all_comments,
    get_comments_offset,
    new_rentType,

)

from wsgi import app
from datetime import datetime,timedelta

LOGGER = logging.getLogger(__name__)

class NotesUnitTest(unittest.TestCase):
    def test_create_note(self):
        date = datetime.now().date()
        new_note = Notes(1,'Test Comment', date)
        assert new_note.rent_id == 1
        assert new_note.comment == 'Test Comment'
        assert new_note.date_created == date

    def test_create_note_toJSON(self):
        date = datetime.now().date()
        new_note = Notes(1,'Test2Comment', date)
        expected_json = {
            "id":None,
            "rent_id":1,
            "comment":"Test2Comment",
            "date_created":datetime.strftime(date,'%Y-%m-%d')
        }
        self.assertDictEqual(expected_json, new_note.toJSON())

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"/App/py_test.db")

class NotesIntegratedTest(unittest.TestCase):
    def test_create_comment(self):
        date = datetime.now()
        area = add_new_area('NotesTestArea',12,12)
        locker = add_new_locker('NotesLocker','Large','Free','NotesKey',area.id)
        student = add_new_student('00001111','Notes','StudentTest','TST','18008001234','notes@email.com')
        rentType = new_rentType(date, timedelta(days=1825) + date,'SemesterLarge',200)
        rent = create_rent(student.student_id,locker.locker_code,rentType.id,date, timedelta(days=90)+date,'FIXED',None)
        note = create_comment(rent.id,'Student left locker in good condition',date.date())
        assert note.comment == 'Student left locker in good condition'
        assert note.rent_id == rent.id
    
    def test_get_comment(self):
        note = get_comment(1)
        assert note.comment == 'Student left locker in good condition'
        assert note.rent_id == 1
    
    def test_get_comments_all(self):
        date = datetime.strftime(datetime.now(),'%Y-%m-%d')
        notes = get_all_comments(1)
        notes = [n.toJSON() for n in notes]
        expected_list = [{
            "id":1,
            "rent_id":1,
            "comment": 'Student left locker in good condition',
            "date_created":date
        }]
        self.assertListEqual(expected_list,notes)
    
    def test_get_comments_offset(self):
        date = datetime.strftime(datetime.now(),'%Y-%m-%d')
        notes = get_comments_offset(1,6,1)
        expected_list = [{
            "id":1,
            "rent_id":1,
            "comment": 'Student left locker in good condition',
            "date_created":date
        }]
        self.assertIsNotNone(notes)
        self.assertListEqual(expected_list,notes['data'])
        assert notes['num_pages'] == 1
        

