from database import db
from datetime import datetime

class Log (db.Model):
    id = db.Column(db.Integer, nullable= False)
    message = db.Column(db.String, nullable=False)
    timestamp =  db.Column(db.DateTime, primary_key = True)


    def __init__(self, id, message,timestamp):
        self.id = id
        self.message = message
        self.timestamp =  datetime.strptime(timestamp,'%Y-%m-%dT%H:%M')
        
            
    def toJSON(self):
        return {
            'id': self.id,
            'message':self.message,
            'timestamp': self.timestamp,
        }