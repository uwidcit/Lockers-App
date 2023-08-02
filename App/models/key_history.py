from App.database import db
from datetime import datetime

class KeyHistory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key_id = db.Column(db.String, db.ForeignKey("locker_keys_table.key_id"), nullable=False)
    locker_id = db.Column(db.String, db.ForeignKey("locker.locker_code"), nullable=False)
    date_moved = db.Column(db.Date, nullable=False, default= datetime.now().date())
    Rent = db.relationship('Rent',backref='key_history', lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self,key_id,locker_id,date_moved):
        self.key_id = key_id
        self.locker_id = locker_id
        self.date_moved = date_moved
    
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
            "rent":self.getRents()
        }