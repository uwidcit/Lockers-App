from database import db

class Area(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    description = db.Column(db.String, nullable = False)
    longitude = db.Column (db.Float, nullable = False)
    latitude = db.Column (db.Float, nullable = False)
    locker = db.relationship('Locker', backref='Area',lazy=True, cascade="all, delete-orphan")

    def __init__(self, description, longitude, latitude):
        self.description = description
        self.longitude = longitude
        self.latitude = latitude

    def toJSON(self):
        return {
            'id':self.id,
            'description':self.description,
            'longitude':self.longitude,
            'latitude':self.latitude,
        }
    
    def getLockersInArea(self):
        if not self.locker:
            return None
        return [l.toJSON() for l in self.locker]
