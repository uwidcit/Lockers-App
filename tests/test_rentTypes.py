import os, pytest, logging, unittest
from models import RentTypes
from datetime import datetime

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
        new_rentType = RentTypes(period_from,period_to,'Semester',400)

        expected_json = {
            'id':None,
            'period_from': period_from,
            'period_to': period_to,
            'type':'Semester',
            'price':400
        }
        self.assertDictEqual(expected_json,new_rentType.toJSON())
