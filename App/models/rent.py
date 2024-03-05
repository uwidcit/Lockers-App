from datetime import datetime
from App.database import db
from math import floor
from enum import Enum

class RentStatus(Enum):
    PARTIAL = "Partial"
    RETURNED = "Returned"
    PAID = "Paid"
    OWED = "Owed"
    OVERDUE = "Overdue"
    VERIFIED = "Verified"

class RentMethod(Enum):
    RATE = "Rate"
    FIXED = "Period"

class Rent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column (db.String, db.ForeignKey("student.student_id"), nullable= False)
    keyHistory_id = db.Column(db.Integer, db.ForeignKey("key_history.id"), nullable= False)
    rent_type =  db.Column(db.Integer, db.ForeignKey("rental_types.id"), nullable= False)
    rent_method = db.Column(db.Enum(RentMethod), nullable = False)
    rent_date_from =  db.Column(db.DateTime, nullable= False)
    rent_date_to = db.Column(db.DateTime, nullable= False)
    date_returned = db.Column(db.DateTime, nullable = True)
    amount_owed = db.Column(db.Float, nullable= False)
    amount_paid = db.Column(db.Float, nullable= False, default=0)
    additional_fees = db.Column(db.Float, nullable= False, default=0)
    late_fees = db.Column(db.Float, nullable = False, default=0)
    status = db.Column(db.Enum(RentStatus), nullable = False)
    Transactions = db.relationship('TransactionLog', backref='rent', lazy=True, cascade="all, delete-orphan")

    def __init__(self, student_id,  keyHistory_id, rent_type, rent_date_from, rent_date_to,amount_owed,rent_method,date_returned):
        self.student_id = student_id
        self.keyHistory_id = keyHistory_id
        self.rent_type =  rent_type
        self.rent_date_from =  rent_date_from
        self.rent_date_to  =  rent_date_to
        self.amount_owed = amount_owed
        self.amount_paid  = 0
        self.date_returned = date_returned
        self.status = self.check_status()
        if rent_method.upper() in RentMethod.__members__:
            self.rent_method = RentMethod[rent_method.upper()]
    
    def check_status(self):
        timestamp =datetime.now()
        timestamp.replace(microsecond=0)
        if self.amount_paid <= 0:
            if timestamp > self.rent_date_to and not self.date_returned:
                return RentStatus.OVERDUE
            return RentStatus.OWED
        else:
            if self.amount_paid < self.amount_owed:
                return RentStatus.PARTIAL
            elif self.cal_amount_owed() == 0:
                if self.date_returned:
                    if self.status == RentStatus.VERIFIED:
                        return RentStatus.VERIFIED
                    return RentStatus.RETURNED
                return RentStatus.PAID
            return RentStatus.OWED

    def cal_amount_owed(self):
        return (self.amount_owed + self.late_fees+ self.additional_fees) - self.amount_paid
    
    def update_payments(self,amount_paid):
        self.amount_paid = self.amount_paid + float(amount_paid)
        self.check_status()

    def cal_additional_fees(self,new_fees):
        self.additional_fees = self.additional_fees + float(new_fees)
        self.check_status()
        
    def toJSON(self):
        rent_dict =  {
            "id":self.id,
            "student_id" : self.student_id,
            "keyHistory_id":  self.keyHistory_id,
            "rent_method": self.rent_method.value,
            "rent_type": self.rent_type,
            "rent_date_from": datetime.strftime(self.rent_date_from,'%Y-%m-%d %H:%M:%S'),
            "rent_date_to": datetime.strftime(self.rent_date_to,'%Y-%m-%d %H:%M:%S'),
            "amount_owed":self.cal_amount_owed(),
            "additional_fees":self.additional_fees,
            "late_fees":self.late_fees,
            "status":self.check_status().value
            }
        if not self.date_returned:
         rent_dict.update({'date_returned':''})
        else:
            rent_dict.update({'date_returned':datetime.strftime(self.date_returned,'%Y-%m-%d %H:%M:%S')})
        return rent_dict