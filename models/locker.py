import string
from database import db
from enum import Enum

class Status(Enum):
    RENTED = "Rented"
    REPAIR = "Repair"
    FREE = "Free"

class Locker (db.Model):
    locker_code = db.Column(db.String, primary_key= True)
    area = db.Column(db.Integer, db.ForeignKey('area.id') ,nullable = False)
    locker_type = db.Column(db.Integer, db.ForeignKey('locker_types.id'),nullable = False)
    status = db.Column(db.Enum(Status), nullable=False)
    key_id = db.Column(db.String, db.ForeignKey('key.key_id') ,nullable = False)

    def __init__(self,locker_code,area,locker_type,status,key_id):
        self.locker_code = locker_code
        self.area = area
        self.locker_type = locker_type
        if string.upper(status) in Status.__members__:
            self.status = Status[string.upper(status)]
        self.key_id = key_id
    
    def toJSON(self):
        return {
            'locker_code': self.locker_code,
            'area': self.area.location,
            'locker_type':self.locker_type.locker_type,
            'status': self.status.name,
            'key_id':self.key_id
        }