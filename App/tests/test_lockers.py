import os, pytest, logging, unittest
from App.main import create_app
from App.database import create_db
from App.models import Locker
from App.models.locker import LockerStatus as Status,LockerTypes 
from App.controllers import (
    add_new_area,
    get_locker_id_locker,
    get_current_locker_instance,
    add_new_locker,
    add_new_student,
    new_rentType,
    get_lockers_available,
    get_locker_by_area_id_toJSON,
    get_locker_id,
    get_all_lockers,
    getLockerTypes,
    getStatuses,
    rent_locker,
    release_locker,
    update_locker_area,
    delete_locker,
    not_verified,
    update_key,
    update_locker_type,
    update_locker_status,
    swap_key,
    create_rent,
    get_locker_rent_history,
    get_current_rental_c,
)

from wsgi import app
from datetime import datetime,timedelta

LOGGER = logging.getLogger(__name__)

class LockerUnitTests(unittest.TestCase):

    def test_new_locker(self):
        new_locker = Locker('A1001','MEDIUM','FREE',2)
        assert new_locker.locker_code =='A1001' 
        assert new_locker.locker_type.value == 'Medium' 
        assert new_locker.status.value == 'Free'
        assert new_locker.area == 2

    def test_new_locker_toJSON(self):
        new_locker = Locker('A2010','SMALL','RENTED', 1)

        expected_json = {
            'locker_code':'A2010',
            'locker_type':'Small',
            'status':'Rented',
            'area': 1
            }
        self.assertDictEqual(new_locker.toJSON(),expected_json)

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+"/App/py_test.db")
    

class LockerIntegrationTests(unittest.TestCase):
    def test_add_new_locker(self):
        new_area = add_new_area('A locker description',10.283759,-61.404937)
        new_locker = add_new_locker('A1001','MEDIUM','FREE','test01', 1)
        self.assertIsNotNone(new_locker)
        assert new_locker.locker_code =='A1001' 
        assert new_locker.locker_type.value == 'Medium' 
        assert new_locker.status.value == 'Free'
        assert new_locker.area == 1
    
    def test_add_new_locker_duplicate(self):
        new_locker = add_new_locker('A1001','MEDIUM','FREE','TEST', 1)
        self.assertIsNone(new_locker)
    
    def test_get_available_lockers(self):
        result = get_lockers_available()
        expected_list = [{
            'locker_code':'A1001',
            'locker_type':'Medium',
            'status':'Free',
            'area': 1
            }]
        self.assertListEqual(expected_list, result)
    
    def test_get_all_lockers(self):
        result = get_all_lockers()
        expected_list = [{
            'locker_code':'A1001',
            'locker_type':'Medium',
            'status':'Free',
            'key': 'test01',
            'area': 1,
            'area_description': 'A locker description'
            }]
        self.assertListEqual(expected_list, result)

    def test_rent_locker(self):
        result = rent_locker('A1001')
        self.assertTrue(result)
        locker = get_locker_id_locker('A1001')
        assert locker.status == Status.RENTED

    def test_rent_locker_rented(self):
        result = rent_locker('A1001')
        self.assertIsNone(result)
    
    def test_rent_locker_invalid(self):
        result = rent_locker('A1241')
        self.assertIsNone(result)

    def test_release_locker(self):
        keyHistoryID = get_current_locker_instance('A1001')
        result = release_locker(keyHistoryID.id)
        self.assertTrue(result)
        locker = get_locker_id_locker('A1001')
        assert locker.status == Status.FREE
    
    def test_release_locker_invalid(self):
        result = release_locker(654321)
        self.assertIsNone(result)
    
    def test_not_verified(self):
        keyHistoryID = get_current_locker_instance('A1001')
        result = not_verified(keyHistoryID.id)
        self.assertTrue(result)
        locker = get_locker_id_locker('A1001')
        assert locker.status == Status.NVERIFIED
    
    def test_not_verified_invalid(self):
        result = not_verified(654321)
        self.assertIsNone(result)
    
    def test_delete_locker(self):
        add_new_locker('A1111','COMBINATION','RENTED','TEST', 1)
        locker = delete_locker('A1111')
        self.assertIsNotNone(locker)
        self.assertIsNone(get_locker_id('A1111'))
    
    def test_delete_locker_invalid(self):
        result = delete_locker('A1241')
        self.assertIsNone(result)

    def test_update_locker_type_small(self):
         locker = update_locker_type('A1001','Small')
         assert locker.locker_type == LockerTypes.SMALL

    def test_update_locker_type_combination(self):
         locker = update_locker_type('A1001','Combination')
         assert locker.locker_type == LockerTypes.COMBINATION

    def test_update_locker_type_medium(self):
         locker = update_locker_type('A1001','Medium')
         assert locker.locker_type == LockerTypes.MEDIUM

    def test_update_locker_type_invalid(self):
         locker = update_locker_type('A1001','Circle')
         self.assertIsNone(locker)

    def test_update_locker_status_rented (self):
         locker = update_locker_status('A1001','Rented')
         assert locker.status == Status.RENTED
    
    def test_update_locker_status_repair (self):
         locker = update_locker_status('A1001','Repair')
         assert locker.status == Status.REPAIR

    def test_update_locker_status_free (self):
         locker = update_locker_status('A1001','Free')
         assert locker.status == Status.FREE
    
    def test_update_locker_status_invalid (self):
         locker = update_locker_status('A1001','Broken')
         self.assertIsNone(locker)
    
    def test_getStatuses(self):
        expectedList =['Rented','Repair','Free','Not Verified']
        result = getStatuses()
        self.assertListEqual(expectedList,result)
    
    def test_getLockerTypes(self):
        expectedList =['Small','Medium','Large','Combination']
        result = getLockerTypes()
        self.assertListEqual(expectedList,result)

    def test_swap_key(self):
        locker1 = add_new_locker('A2001','MEDIUM','FREE','K201', 1)
        locker2 = add_new_locker('A3001','MEDIUM','FREE','K301', 1)
        result = swap_key(locker1.locker_code, locker2.locker_code)
        assert result[0][2].key_id == 'K301'
        assert result[1][2].key_id == 'K201'

    def test_swap_key_invalid(self):
        result = swap_key('invalid', 'invalid2')
        self.assertIsNone(result)

    def test_update_key(self):
        update = update_key('A1001', 'K101')
        locker = get_locker_id('A1001')
        assert locker[2].key_id == 'K101'

    def test_update_key_invalid_key(self):
        with pytest.raises(Exception) as e:
            update = update_key('A1001', None)
            update2 = update_key('A1001', '')
            assert str(e) == 'Key cannot be empty'

    def test_update_key_invalid_locker(self):
        update = update_key('A1001', 'K101')
        self.assertIsNone(update)
    
    def test_get_lockers_by_area_id(self):
        lockers = get_locker_by_area_id_toJSON(1)
        expected_list = [{
            'locker_code':'A1001',
            'locker_type':'Medium',
            'status':'Free',
            'area': 1,
            }]
        self.assertListEqual(expected_list, lockers)
    
    def test_update_locker_area(self):
        new_area = add_new_area('An area description',10.283759,-61.404937)
        new_locker = add_new_locker('TEST10101','MEDIUM','FREE','test01', new_area.id)
        result = update_locker_area(new_locker.locker_code,new_area.id)
        assert result.locker_code == 'TEST10101'
        assert result.area == new_area.id
    
    def test_get_current_rental_c(self):
        new_area = add_new_area('Area3?',10.283759,-61.404937)
        new_locker = add_new_locker('NewLocker2','MEDIUM','FREE','TestlockerKey', new_area.id)
        add_new_student('123456789','Victory','Friends','FSS','18684981333','victoria.friends@my.uwi.edu')
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent_type = new_rentType(period_from,period_to,'Daily',4)
        rent_period_from = datetime.now()
        rent_period_from = rent_period_from.replace(hour = 8, minute = 0 ,second= 0, microsecond= 0)
        rent_period_to = rent_period_from + timedelta(days=5)
        create_rent('123456789','NewLocker2',1,rent_period_from,rent_period_to, 'RATE', None)
        rent = get_current_rental_c('NewLocker2')
        assert rent.student_id == '123456789'
        assert rent.rent_type == 1
        assert rent.rent_date_from == rent_period_from
        assert rent.rent_date_to == rent_period_to
        assert rent.date_returned is None
        assert rent.amount_owed == 20
        assert rent.status.value == 'Owed'
    
    def test_get_locker_rent_history(self):
        rent_period_from = datetime.now()
        rent_period_from = rent_period_from.replace(hour = 8, minute = 0 ,second= 0, microsecond= 0)
        rent_period_to = rent_period_from + timedelta(days=5)
        locker_rents = get_locker_rent_history('NewLocker2',6,1)
        expected_list= [{
            'id': 1,
            'student_id': '123456789',
            'keyHistory_id':2,
            "additional_fees":0.0,
            'late_fees':0.0,
            'rent_type':1,
            'rent_method':'Rate',
            'rent_date_from':datetime.strftime(rent_period_from,'%Y-%m-%d %H:%M:%S'),
            'rent_date_to':datetime.strftime(rent_period_to,'%Y-%m-%d %H:%M:%S'),
            'date_returned':"",
            'amount_owed':20.0,
            'status':'Owed'
        }]
        self.assertListEqual(expected_list, locker_rents["data"])






    
