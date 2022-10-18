from database import db

class Area(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    location = db.Column(db.String, nullable = False)
    lockers = db.relationship('Locker', backref='areas', lazy=True, cascade="all, delete-orphan")


    def __init__(self,location):
        self.location = location

    def toJSON(self):
        return {
            'id':self.id,
            'location':self.location,
            'lockers': [l.toJSON() for l in self.lockers]
        } 
