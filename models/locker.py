from database import db
from enum import Enum

class Status(Enum):
    RENTED = "Rented"
    REPAIR = "Repair"
    FREE = "Free"

class LockerTypes(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    COMBINATION = "Combination"

class Key(Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
    LOST = "Lost"

class Locker (db.Model):
    locker_code = db.Column(db.String, primary_key= True)
    locker_type = db.Column(db.Enum(LockerTypes),nullable = False)
    status = db.Column(db.Enum(Status), nullable=False)
    key = db.Column(db.Enum(Key) ,nullable = False)
    area = db.relationship('Area', backref='locker', lazy=True, cascade="all, delete-orphan")

    def __init__(self,locker_code,locker_type,status,key):
        self.locker_code = locker_code
        if status.upper() in Status.__members__:
            self.status = Status[status.upper()]
        if locker_type.upper() in LockerTypes.__members__:
            self.locker_type = LockerTypes[locker_type.upper()]
        if key.upper() in Key.__members__:
            self.key = Key[key.upper()]
            
    def toJSON(self):
        return {
            'locker_code': self.locker_code,
            'locker_type':self.locker_type.name,
            'status': self.status.name,
            'key':self.key.name,
        }