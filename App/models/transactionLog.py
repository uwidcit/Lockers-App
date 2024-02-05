from datetime import datetime
from App.database import db
from enum import Enum

from sqlalchemy import Sequence

seq = Sequence('transaction_log_receipt_number_seq')

class TransactionType(Enum):
    CREDIT = "credit"
    DEBIT = "debit"

class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rent_id = db.Column(db.Integer, db.ForeignKey("rent.id"), nullable = False)
    currency = db.Column(db.String(3), nullable=False)
    transaction_date = db.Column(db.Date,nullable = False)
    amount = db.Column(db.Float , nullable = False)
    description = db.Column(db.String, nullable = False)
    receipt_number = db.Column(db.Integer,seq,nullable=False,unique=True)
    type = db.Column(db.Enum(TransactionType), nullable = False)

    def __init__(self, rent_id, currency, transaction_date, amount, description, type):
        self.rent_id = rent_id
        self.currency = currency
        self.transaction_date = transaction_date
        self.amount = amount
        self.description = description
        if type.upper() in TransactionType.__members__:
            self.type = TransactionType[type.upper()]
    
    def toJSON(self):
        return {
            "id": self.id,
            "rent_id":self.rent_id,
            "currency":self.currency,
            "transaction_date":self.transaction_date,
            "amount":self.amount,
            "description": self.description,
            "type":self.type.value,
            "receipt_number":self.receipt_number
        }
