from App.database import db 
from App.models import TransactionLog,Rent
from datetime import datetime
from flask import flash
from App.controllers.log import create_log
from App.models.transactionLog import TransactionType
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

def add_new_transaction(rent_id, currency, transaction_date, amount, description, t_type,receipt_number):
    try:
        new_transaction = TransactionLog(rent_id, currency,transaction_date, amount, description, t_type,receipt_number)
        rent = Rent.query.filter_by(id=rent_id).first()
        rent.update_payments(amount)
        db.session.add(new_transaction)
        db.session.add(rent)
        db.session.commit()
        return new_transaction
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

def get_transaction_id(id):
    transaction = TransactionLog.query.filter_by(id = id).first()

    if not transaction:
        flash("Transaction does not exist")
        return None
    return transaction

def get_transaction_json(id):
    transaction = get_transaction_id(id)

    if not transaction:
        return None
    return transaction.toJSON()

def get_transaction_by_receipt_number(receipt_no):
    transaction = TransactionLog.query.filter_by(receipt_no = receipt_no).first()

    if not transaction:
        return None
    return transaction

def get_transaction_by_receipt_number_json(id):
    transaction = get_transaction_by_receipt_number(id)

    if not transaction:
        return None
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
    return round(amount,2)

def get_all_transactions():
    transactions = TransactionLog.query.all()

    if not transactions:
        return []

    return [t.toJSON() for t in transactions]

def get_num_transactions():
    trans = TransactionLog.query.all()
    if not trans:
        return 1
    
    return len(trans)
   

def get_num_transactions_page(size):
    count = get_num_transactions()
    if count == 0:
        return 1

    if count%size != 0:
        return int(count/size + 1)
    return int(count/size)

def get_transactions_by_offset(size, offset):
    t_offset = (offset * size) - size
    transactions = TransactionLog.query.order_by(TransactionLog.id.desc()).limit(size).offset(t_offset)
        
    if not transactions:
        return None
    return [t.toJSON() for t in transactions]

def getT_Type():
    return [ e.value for e in TransactionType ]

def search_transaction(query,size,offset):
    try:
        int_query = int(query)
        data = db.session.query(TransactionLog,Rent).join(Rent).filter(or_(TransactionLog.id == int_query,TransactionLog.rent_id == int_query, Rent.student_id == int_query, TransactionLog.receipt_number == int_query, TransactionLog.amount== int_query)).all()
    except:
        if query.upper() in TransactionType.__members__:
            data = db.session.query(TransactionLog,Rent).join(Rent).filter((TransactionLog.type == TransactionType[query.upper()])).all()
        else:
            data = db.session.query(TransactionLog,Rent).join(Rent).filter(or_(TransactionLog.currency.contains(query), TransactionLog.description.contains(query))).all()


    if not data:
        return None
    length_transactions = len(data)
    if length_transactions == 0:
         num_pages = 1
    
    if length_transactions%size != 0:
        num_pages = int((length_transactions/size) + 1)
    else:
        num_pages = int(length_transactions/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop > length_transactions):
        stop = length_transactions
    
    t_list = []
    for transactions,rent in data[index:stop]:
        t_list.append(transactions.toJSON())
    return {"num_pages": num_pages,"data":t_list}

    