import os, pytest, logging, unittest
from App.models import RentTypes
from App.models.rentTypes import Types
from App.main import create_app
from App.database import create_db
from App.controllers import (
    new_rentType,
    delete_rent_type,
    get_All_rentType,
    get_rentType_by_id,
    update_rentType_period,
    update_rentType_price,
    update_rentType_type,
)
from datetime import datetime
from wsgi import app

LOGGER = logging.getLogger(__name__)

class RentTypeUnitTests(unittest.TestCase):
    def test_new_rentType(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        new_rentType = RentTypes(period_from,period_to,'Daily',4)
        assert new_rentType.period_from == period_from
        assert new_rentType.period_to == period_to
        assert new_rentType.type == 'Daily'
        assert new_rentType.price == 4
    
    def test_new_rentType(self):
        period_from = datetime(2021,8,31)
        period_to = datetime(2022,7,31)
        new_rentType = RentTypes(period_from,period_to,'SEMESTERMEDIUM',400)

        expected_json = {
            'id':None,
            'period_from': datetime.strftime(period_from,'%Y-%m-%d'),
            'period_to': datetime.strftime(period_to,'%Y-%m-%d'),
            'type': 'Semester Medium',
            'price':400
        }
        self.assertDictEqual(expected_json,new_rentType.toJSON())

@pytest.fixture(autouse=True, scope="class")
def empty_db():
    os.unlink(os.getcwd()+"/App/py_test.db")
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///py_test.db'})
    create_db(app)
    yield app.test_client()
    

class RentTypeIntegerationTest(unittest.TestCase):
    def test_new_rentType(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        new_Type = new_rentType(period_from,period_to,'Daily',4)
        self.assertIsNotNone(new_Type)
        assert new_Type.id == 1
        assert new_Type.period_from == period_from.date()
        assert new_Type.period_to == period_to.date()
        assert new_Type.price == 4
    
    def test_update_rentType_price(self):
        result = update_rentType_price(1,8)
        assert result.price == 8
    
    def test_update_rentType_price_invalid(self):
        result = update_rentType_price(0,800)
        self.assertIsNone(result)

    def test_update_rentType_period(self):
        period_from = datetime(2021,8,31)
        period_to = datetime(2022,7,31)
        result = update_rentType_period(1,period_from,period_to)
        assert result.period_from == period_from.date()
        assert result.period_to == period_to.date()
    
    def test_update_rentType_period_invalid(self):
        period_from = datetime(2021,8,31)
        period_to = datetime(2022,7,31)
        result = update_rentType_period(0,period_from,period_to)
        self.assertIsNone(result)
    
    def update_rentType_type_hourly(self):
        result = update_rentType_type(1,'Hourly')
        assert result.type == Types.HOURLY

    def update_rentType_type_z_daily(self):
        result = update_rentType_type(1,'Daily')
        assert result.type == Types.DAILY
    
    def test_rentType_delete(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        rent = new_rentType(period_from,period_to,'Daily',4)
        result = delete_rent_type(rent.id)
        self.assertIsNotNone(result)
        self.assertIsNone(get_rentType_by_id(2))
    
    def test_rentType_delete_invalid(self):
        result = delete_rent_type(45)
        self.assertIsNone(result)
    
    def test_rentType_get_all(self):
        period_from = datetime(2022,8,31)
        period_to = datetime(2023,7,31)
        expectedList =[{
            'id':1,
            'period_from': datetime.strftime(period_from,'%Y-%m-%d'),
            'period_to': datetime.strftime(period_to,'%Y-%m-%d'),
            'type':'Daily',
            'price':4
        }]
        
        self.assertListEqual(expectedList, get_All_rentType())
