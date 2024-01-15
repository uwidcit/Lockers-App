from App.database import db
from App.models import KeyHistory,Active
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

def new_keyHistory(key_id,locker_id,date_moved):
    try:
        newkeyHistory = KeyHistory(key_id,locker_id,date_moved,"Active")
        db.session.add(newkeyHistory)
        db.session.commit()
        return newkeyHistory
    except SQLAlchemyError as e:
        db.session.rollback()
        return None
    
def restore_keyHistory(id,key_id,locker_id,date_moved):
    try:
        keyHistory = KeyHistory(key_id,locker_id,date_moved,"Active")
        keyHistory.id = id 
        db.session.add(keyHistory)
        db.session.commit()
        return keyHistory
    except SQLAlchemyError as e:
        db.session.rollback()
        return None
    
def deactivate(id):
    keyH = getKeyHistory(id)
    if not keyH:
        return None
    keyH.isActive = Active.INACTIVE
    try:
        db.session.commit()
        return keyH
    except:
        db.session.rollback()
        return None

def getKeyHistory(id):
    key = KeyHistory.query.filter_by(id=id).first()

    if not key:
        return None
    return key

def getKeyHistory_by_id(id, size,offset):
    keys = KeyHistory.query.filter(or_(KeyHistory.locker_id.contains(id),KeyHistory.key_id.contains(id))).all()

    if not keys:
        return None

    length_keys = len(keys)
    if length_keys == 0:
        num_pages = 1
    elif length_keys%size != 0:
        num_pages  = int((length_keys/size)+1)
    else:
        num_pages = int(length_keys/size)
    
    index = (offset * size) - size
    stop = (offset * size)
    if(stop > length_keys):
        stop = length_keys
    k_list = []

    for d in keys[index:stop]:
        k_list.append(d.toJSON())
    return {'num_pages':num_pages, "data":k_list}

def changeDateMove(id,newDate):
    key = KeyHistory.query.filter_by(id = id).first()

    if not key:
        return None

    try:
         key.date_moved = newDate
         db.session.add(key)
         db.session.commit()
         return key
    except:
        db.session.rollback()
        return None


def getKeyHistory_all(size,offset):
    keys = KeyHistory.query.all()

    if not keys:
        return None

    length_keys = len(keys)
    if length_keys == 0:
        num_pages = 1
    elif length_keys%size != 0:
        num_pages  = int((length_keys/size)+1)
    else:
        num_pages = int(length_keys/size)
    
    index = (offset * size) - size
    stop = (offset * size)
    if(stop > length_keys):
        stop = length_keys
    k_list = []

    for d in keys[index:stop]:
        k_list.append(d.toJSON())
    return {'num_pages':num_pages, "data":k_list}
    
