from App.database import db
from datetime import datetime
from enum import Enum

class Key_Status(Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
    LOST = "Lost"
    CUTTING = "Cutting"
    READY = "Ready"


class Key(db.Model):
    __tablename__ = 'locker_keys_table'
    key_id = db.Column(db.String, primary_key = True)
    masterkey_id  = db.Column (db.String, db.ForeignKey("masterkey.masterkey_id"),nullable = False)
    key_status = db.Column(db.Enum(Key_Status),nullable = False)
    date_added = db.Column (db.Date, nullable = False)
    KeyH = db.relationship('KeyHistory', backref='key', lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, key_id,masterkey_id,key_status, date_added):
        self.key_id = key_id
        self.masterkey_id = masterkey_id
        if key_status.upper() in Key_Status.__members__:
            self.key_status = Key_Status[key_status.upper()]
        self.date_added = date_added
    
    def toJSON(self):
        from App.models import KeyHistory
        keyHistory = self.KeyH.order_by(KeyHistory.id.desc()).first()
        return{
            'key_id':self.key_id,
            'masterkey_id':self.masterkey_id,
            'key_status':self.key_status.value,
            'date_added': datetime.strftime(self.date_added,'%Y-%m-%d'),
            'KeyHistory': keyHistory.toJSON(),
        }