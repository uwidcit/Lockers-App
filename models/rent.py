from database import db

class Rent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column (db.Integer, db.ForeignKey("student.student_id"), nullable= False)
    locker_id = db.Column(db.String, db.ForeignKey("locker.locker_code"), nullable= False)
    rent_type =  db.Column(db.Integer, db.ForeignKey("RentType.id"), nullable= False)
    rent_date_from =  db.Column(db.Date, nullable= False)
    rent_date_to = db.Column(db.Date, nullable= False)
    date_returned = db.Column(db.Date, nullable = True)
    amount_owed = db.Column(db.Float, nullable= False)

    def __init__(self, student_id, locker_id, rent_type, rent_date_from, rent_date_to,date_returned,amount_owed):
        self.student_id = student_id
        self.locker_id = locker_id
        self.rent_type = rent_type,
        self.rent_date_from = rent_date_from
        self.rent_date_to  = rent_date_to
        self.date_returned = date_returned
        self.amount_owed = amount_owed
        
    def toJSON(self):
        return {
            "student_id" : self.student_id,
            "locker_id":  self.locker_id,
            "rent_type": self.rent_type,
            "rent_date_from": self.rent_date_from,
            "rent_date_to": self.rent_date_to,
            "date_returned":self.date_returned,
            "amount_owed":self.amount_owed,
        }