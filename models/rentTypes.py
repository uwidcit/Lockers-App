from database import db
from enum import Enum
from datetime import datetime

class Types (Enum):
    HOURLY = "Hourly"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    SEMESTER = "Semester"

class RentTypes(db.Model):
    __tablename__= "RentTypes"
    id = db.Column(db.Integer, primary_key = True)
    period_from = db.Column(db.Date, nullable = False)
    period_to = db.Column(db.Date, nullable = False)
    type = db.Column(db.Enum(Types), nullable = False)
    price = db.Column(db.Float, nullable = False)

    def __init__(self, period_from,period_to,type,price):
        self.period_from = period_from
        self.period_to = period_to
        if type.upper() in Types.__members__:
            self.type = Types[type.upper()]
        self.price = price
    
    def toJSON(self):
        return {
            "id":self.id,
            "period_from": datetime.strftime(self.period_from,'%Y-%m-%d'),
            "period_to": datetime.strftime(self.period_to,'%Y-%m-%d'),
            "type":  self.type.value,
            "price": self.price,
        }
        