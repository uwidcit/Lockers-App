from models import TransactionLog
from database import db 
from sqlalchemy.exc import SQLAlchemyError

def create_transaction(rent_id, currency,transaction_date, amt, description, type):
    try:
        new_transaction = TransactionLog(rent_id,currency,transaction_date,amt,description,type)
        db.session.add(new_transaction)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return None

def get_transaction(id):
    transaction = TransactionLog.query.filter_by(id= id).first()

    if not transaction:
        return None

    return transaction

def get_transaction_toJSON(id):
    transaction = get_transaction(id)

    if not transaction:
        return None

    return transaction.toJSON()