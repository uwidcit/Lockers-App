from datetime import datetime
from database import db
from enum import Enum

class Status(Enum):
    PARTIAL = "Partial"
    RETURNED = "Returned"
    PAID = "Paid"
    OWED = "Owed"
    OVERDUE = "Overdue"
    VERIFIED = "Verified"

class Rent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column (db.Integer, db.ForeignKey("student.student_id"), nullable= False)
    locker_id = db.Column(db.String, db.ForeignKey("locker.locker_code"), nullable= False)
    rent_type =  db.Column(db.Integer, db.ForeignKey("RentTypes.id"), nullable= False)
    rent_date_from =  db.Column(db.DateTime, nullable= False)
    rent_date_to = db.Column(db.DateTime, nullable= False)
    date_returned = db.Column(db.DateTime, nullable = True)
    amount_owed = db.Column(db.Float, nullable= False)
    status = db.Column(db.Enum(Status), nullable = False)
    Transactions = db.relationship('TransactionLog', backref='rent', lazy=True, cascade="all, delete-orphan")

    def __init__(self, student_id, locker_id, rent_type, rent_date_from, rent_date_to,amount_owed):
        self.student_id = student_id
        self.locker_id = locker_id
        self.rent_type =  rent_type
        self.rent_date_from =  rent_date_from
        self.rent_date_to  =  rent_date_to
        self.amount_owed = amount_owed
        self.status = self.check_status()
    
    def check_status(self):
        timestamp =datetime.now()
        timestamp.replace(microsecond=0)
        if not self.Transactions:
            if timestamp > self.rent_date_to and not self.date_returned:
                return Status.OVERDUE
            return Status.OWED
        else:
            amount = self.cal_transactions()
            if amount < self.amount_owed:
                return Status.PARTIAL
            elif self.amount_owed == 0:
                if self.date_returned:
                    if self.status == Status.VERIFIED:
                        return Status.VERIFIED
                    return Status.RETURNED
                return Status.PAID
            return Status.OWED

    def cal_transactions(self):
        if not self.Transactions:
            return 0
        amount = 0
        for t in self.Transactions:
            amount += float(t.amount)
        return amount
    
    def toJSON(self):
        return {
            "id":self.id,
            "student_id" : self.student_id,
            "locker_id":  self.locker_id,
            "rent_type": self.rent_type,
            "rent_date_from": self.rent_date_from,
            "rent_date_to": self.rent_date_to,
            "date_returned":self.date_returned,
            "amount_owed":self.amount_owed,
            "status":self.check_status().value
        }