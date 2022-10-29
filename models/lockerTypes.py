from database import db

class LockerTypes(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    locker_type = db.Column(db.String, nullable = False, unique=True)
    price = db.Column(db.Float, nullable = False)
    lockers = db.relationship('Locker', backref='locker_types', lazy=True, cascade="all, delete-orphan")

    def __init__(self, locker_type,price):
        self.locker_type = locker_type
        self.price = price
    
    def toJSON(self):
        return{
            'id':self.id,
            'locker_type':self.locker_type,
            'price':self.price,
            'lockers': [l.toJSON for l in self.lockers]
        }