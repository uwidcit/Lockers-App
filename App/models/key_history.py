from App.database import db
from enum import Enum
from datetime import datetime

class Active(Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

class KeyHistory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key_id = db.Column(db.String, db.ForeignKey("locker_keys_table.key_id"), nullable=False)
    locker_id = db.Column(db.String, db.ForeignKey("locker.locker_code"), nullable=False)
    date_moved = db.Column(db.Date, nullable=False, default= datetime.now().date())
    isActive = db.Column(db.Enum(Active),nullable=False,default=Active.ACTIVE)
    Rent = db.relationship('Rent',backref='key_history', lazy="select", order_by="Rent.status",cascade="all, delete-orphan")

    def __init__(self,key_id,locker_id,date_moved,isActive):
        self.key_id = key_id
        self.locker_id = locker_id
        self.date_moved = date_moved
        if isActive.upper() is Active.__members__:
            self.isActive = Active[isActive.upper()]
    
    def getRents(self):
        if self.Rent:
            return [r.toJSON() for r in self.Rent]
        else:
            return ''
    
    def toJSON(self):
        return{
            "id":self.id,
            "key_id":self.key_id,
            "locker_id":self.locker_id,
            "date_moved":self.date_moved,
            "isActive":self.isActive.value
        }