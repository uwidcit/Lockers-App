from database import db
from enum import Enum
from datetime import datetime

class Key_Type(Enum):
    COMBINATION = "Combination"
    LOCK = "Lock"

class MasterKey(db.Model):
    __tablename__ = "masterkey"
    id = db.Column(db.Integer, primary_key = True)
    masterkey_id = db.Column(db.String, unique= True, nullable=False)
    series = db.Column(db.String, nullable=False)
    key_type = db.Column(db.Enum(Key_Type), nullable=False)
    date_added = db.Column(db.Date, nullable = False)
    keys = db.relationship('Key', backref='masterkey', lazy=True, cascade="all, delete-orphan")

    def __init__(self,masterkey_id,series,key_type,date_added):
        self.masterkey_id = masterkey_id
        self.series = series
        if key_type.upper() in Key_Type.__members__:
            self.key_type = Key_Type[key_type.upper()]
        self.date_added = date_added

    def toJSON(self):
        return{
            'id':self.id,
            'masterkey_id':self.masterkey_id,
            'series': self.series,
            'key_type': self.key_type.value,
            'date_added':  datetime.strftime(self.date_added,'%Y-%m-%d')}