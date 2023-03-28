from database import db
from datetime import datetime

class KeyHistory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key_id = db.Column(db.String, db.ForeignKey("locker_keys_table.key_id"), nullable=False)
    locker_id = db.Column(db.String, db.ForeignKey("locker.locker_code"), nullable=False)
    date_moved = db.Column(db.Date, nullable=False, default= datetime.now().date())

    def __init__(self,key_id,locker_id,date_moved):
        self.key_id = key_id
        self.locker_id = locker_id
        self.date_moved = date_moved
    
    def toJSON(self):
        return{
            "id":self.id,
            "key_id":self.key_id,
            "locker_id":self.locker_id,
            "date_moved":self.date_moved
        }