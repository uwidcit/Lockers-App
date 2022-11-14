from database import db

class Area(db.Model):
    id = db.Column(db.Integer, primary_key =True)
<<<<<<< HEAD
    location = db.Column(db.String, nullable = False)
    lockers = db.relationship('Locker', backref='areas', lazy=True, cascade="all, delete-orphan")
=======
    locker_id = db.Column(db.Integer, db.ForeignKey('locker.locker_code') ,nullable = False)
    description = db.Column(db.String, nullable = False)
    longitude = db.Column (db.Float, nullable = False)
    latitiude = db.Column (db.Float, nullable = False)
>>>>>>> DB-Modelling

    def __init__(self,locker_id, description, longitude, latitude):
        self.description = description
        self.locker_id = locker_id
        self.longitude = longitude
        self.latitiude = latitude

    def toJSON(self):
        return {
            'id':self.id,
            'locker_id': self.locker_id,
            'description':self.description,
            'longitude':self.longitude,
            'latitiude':self.latitiude,
        } 
