
from database import db
from enum import Enum

class Status(Enum):
    TRUE = True
    FALSE = False

class Key(db.Model):
    key_id = db.Column(db.String, primary_key = True)
    key_1_status = db.Column(db.Enum(Status),nullable=False)
    key_2_status = db.Column(db.Enum(Status),nullable=False)

    def __init__(self, key_id, key_1_status, key_2_status):
       self.key_id = key_id
       if key_1_status.upper() in Status.__members__ and key_2_status.upper() in Status.__members__: 
            self.key_1_status = Status[key_1_status.upper()]
            self.key_2_status = Status[key_2_status.upper()]

    def toggle_key_1_status(self):
        if self.key_1_status is Status.TRUE:
            self.key_1_status = Status.FALSE
        else:
            self.key_1_status = Status.TRUE

    def toggle_key_2_status(self):
        if self.key_2_status is Status.TRUE:
            self.key_2_status = Status.FALSE
        else:
            self.key_2_status = Status.TRUE

    def toJSON(self):
        return{
            'key_id':self.key_id,
            'key_1_status':self.key_1_status.name,
            'key_2_status':self.key_2_status.name,
        }

