from database import db 
from models import TransactionLog
from models.transactionLog import TransactionType
from sqlalchemy.exc import SQLAlchemyError

def add_new_transaction(rent_id, currency, transaction_date, amount, description, t_type,receipt_number):
    try:
        new_transaction = TransactionLog(rent_id, currency,transaction_date, amount, description, t_type,receipt_number)
        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return []

def get_transaction_id(id):
    transaction = TransactionLog.query.filter_by(id = id).first()

    if not transaction:
        return []
    return transaction

def get_transaction_json(id):
    transaction = get_transaction_id(id)

    if not transaction:
        return []
    return transaction.toJSON()

def get_transaction_by_receipt_number(receipt_no):
    transaction = TransactionLog.query.filter_by(receipt_no = receipt_no).first()

    if not transaction:
        return []
    return transaction

def get_transaction_by_receipt_number_json(id):
    transaction = get_transaction_by_receipt_number(id)

    if not transaction:
        return []
    return transaction.toJSON()
    
def get_all_transactions_by_rent(rent_id):
    transactions = TransactionLog.query.filter_by(rent_id= rent_id)

    if not transactions:
        return None
    return transactions

def get_all_transactions_by_rent_json(rent_id):
    transactions = get_all_transactions_by_rent(rent_id=rent_id)
    if not transactions:
        return None
    return [t.toJSON() for t in transactions]

def cal_transaction_amount(rent_id):
    transactions = get_all_transactions_by_rent(rent_id)

    if not transactions:
        return 0.00
    
    amount = 0
    for t in transactions:
        amount =  amount + t.amount
    return amount

def get_all_transactions():
    transactions = TransactionLog.query.all()

    if not transactions:
        return []

    return [t.toJSON() for t in transactions]

def getT_Type():
    return [ e.value for e in TransactionType ]

    