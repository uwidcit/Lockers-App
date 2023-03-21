from database import db
from datetime import datetime
from enum import Enum

class Status(Enum):
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
    status = db.Column(db.Enum(Status), nullable=False)
    key = db.Column(db.String,db.ForeignKey("key.key_id") ,nullable = False)
    area = db.Column(db.Integer, db.ForeignKey("area.id"), nullable=False)
    Rented = db.relationship('Rent', backref='locker', lazy=True, cascade="all, delete-orphan")

    def __init__(self,locker_code,locker_type,status,key,area):
        self.locker_code = locker_code
        if status.upper() in Status.__members__:
            self.status = Status[status.upper()]
        if locker_type.upper() in LockerTypes.__members__:
            self.locker_type = LockerTypes[locker_type.upper()]
        self.key = key
        self.area = area
            
    def toJSON(self):
        return {
            'locker_code': self.locker_code,
            'locker_type':self.locker_type.value,
            'status': self.status.value,
            'key':self.key,
            'area': self.area,
        }

    