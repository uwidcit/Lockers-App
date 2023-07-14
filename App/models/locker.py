from App.database import db
from datetime import datetime
from enum import Enum

class LockerStatus(Enum):
    RENTED = "Rented"
    REPAIR = "Repair"
    FREE = "Free"
    NVERIFIED = "Not Verified"

class LockerTypes(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    COMBINATION = "Combination"

class Locker (db.Model):
    locker_code = db.Column(db.String, primary_key= True)
    locker_type = db.Column(db.Enum(LockerTypes),nullable = False)
    status = db.Column(db.Enum(LockerStatus), nullable=False)
    area = db.Column(db.Integer, db.ForeignKey("area.id"), nullable=False)
    KeyH = db.relationship('KeyHistory', backref='', lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self,locker_code,locker_type,status,area):
        self.locker_code = locker_code
        if status.upper() in LockerStatus.__members__:
            self.status = LockerStatus[status.upper()]
        if locker_type.upper() in LockerTypes.__members__:
            self.locker_type = LockerTypes[locker_type.upper()]
        self.area = area
            
    def toJSON(self):
        return {
            'locker_code': self.locker_code,
            'locker_type':self.locker_type.value,
            'status': self.status.value,
            'area': self.area,
        }
    def get_current_rent(self):
        if not self.Rented:
            return []
        for s in self.Rented:
            if s.status.value != "Verified":
                rent = s.toJSON()
                rent['status'] = rent['status']
                rent['rent_date_from'] = datetime.strftime(rent['rent_date_from'],'%Y-%m-%d')
                rent['rent_date_to'] = datetime.strftime(rent['rent_date_to'],'%Y-%m-%d')
                if s.date_returned:
                    rent['date_returned'] = datetime.strftime(rent['date_returned'],'%Y-%m-%d')
                else:
                    rent['date_returned'] = ""
                return rent
            return []

    