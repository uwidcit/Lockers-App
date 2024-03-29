from App.database import db 
from App.models import TransactionLog,Rent
from App.models.transactionLog import TransactionType
from sqlalchemy import or_,and_,Sequence
from sqlalchemy.exc import SQLAlchemyError

def add_new_transaction(rent_id, currency, transaction_date, amount, description, t_type):
    try:
        new_transaction = TransactionLog(rent_id, currency,transaction_date, amount, description, t_type)
        rent = Rent.query.filter_by(id=rent_id).first()
        rent.update_payments(amount)
        db.session.add(new_transaction)
        db.session.add(rent)
        db.session.commit()
        return new_transaction
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

def restore_transaction(id,rent_id, currency, transaction_date, amount, description, t_type,receipt_number):
    try:
        new_transaction = TransactionLog(rent_id, currency,transaction_date, amount, description, t_type)
        new_transaction.id = id
        new_transaction.receipt_number = id
        rent = Rent.query.filter_by(id=rent_id).first()
        rent.update_payments(amount)
        db.session.add(new_transaction)
        db.session.add(rent)
        seq = Sequence(name='transaction_log_id_seq')
        seq2 = Sequence(name='transaction_log_receipt_number_seq')
        db.session.execute(seq)
        db.session.execute(seq2)
        db.session.commit()
        return new_transaction
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

def get_transaction_id(id):
    transaction = TransactionLog.query.filter_by(id = id).first()

    if not transaction:
        return None
    return transaction

def get_transaction_json(id):
    transaction = get_transaction_id(id)

    if not transaction:
        return None
    return transaction.toJSON()


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
        data = db.session.query(TransactionLog,Rent).join(Rent).filter(or_(TransactionLog.id == int_query,TransactionLog.rent_id == int_query, Rent.student_id == query, TransactionLog.receipt_number == int_query, TransactionLog.amount== int_query)).all()
    except:
        if query.upper() in TransactionType.__members__:
            data = db.session.query(TransactionLog,Rent).join(Rent).filter((TransactionLog.type == TransactionType[query.upper()])).all()
        else:
            return None


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

def get_revenue(start_date, end_date): 
    trans_query = db.session.query(TransactionLog.amount).filter(and_(TransactionLog.transaction_date >= start_date, TransactionLog.transaction_date < end_date)).all()

    if not trans_query:
        return 0  
    sum = 0
    data = []
    for t in trans_query:
        sum += t[0]
        #data.append(t.toJSON())
    return {"sum":sum}

    