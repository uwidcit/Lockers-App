from database import db

class RentType(db.Model):
    __tablename__ = "RentType"
    id = db.Column(db.Integer, primary_key = True)
    period = db.Column(db.String, nullable = False)
    type = db.Column(db.String, nullable = False)
    price = db.Column(db.Float, nullable = False)

    def __init__(self, period,type,price):
        self.period = period
        self.type = type
        self.price = price
    
    def toJSON(self):
        return {
            "id":self.id,
            "period": self.period,
            "type":  self.type,
            "price": self.price,
        }
        