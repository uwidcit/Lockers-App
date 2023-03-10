from database import db
from enum import Enum

class Key_Status(Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
    LOST = "Lost"
    CUTTING = "Cutting"
    READY = "Ready"


class Key(db.Model):
    key_id = db.Column(db.String, primary_key = True)
    masterkey_id  = db.Column (db.Integer, db.ForeignKey("masterkey.id"),nullable = False)
    key_status = db.Column(db.Enum(Key_Status),nullable = False)
    date_added = db.Column (db.Date, nullable = False)

    def __init__(self, key_id,masterkey_id,key_status, date_added):
        self.key_id = key_id
        self.masterkey_id = masterkey_id
        if key_status.upper() in Key_Status.__members__:
            self.key_status = Key_Status[key_status.upper()]
        self.date_added = date_added
    
    def toJSON(self):
        return{
            'key_id':self.key_id,
            'masterkey_id':self.masterkey_id,
            'key_status':self.key_status,
            'date_added':self.date_added
        }