from database import db

class Area(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    locker_id = db.Column(db.Integer, db.ForeignKey('locker.locker_code') ,nullable = False,unique=True)
    description = db.Column(db.String, nullable = False)
    longitude = db.Column (db.Float, nullable = False)
    latitude = db.Column (db.Float, nullable = False)

    def __init__(self,locker_id, description, longitude, latitude):
        self.locker_id = locker_id
        self.description = description
        self.longitude = longitude
        self.latitude = latitude

    def toJSON(self):
        return {
            'id':self.id,
            'locker_id': self.locker_id,
            'description':self.description,
            'longitude':self.longitude,
            'latitude':self.latitude,
        } 
