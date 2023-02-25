from models import MasterKey
from database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_
from datetime import datetime

def new_masterkey(masterkey_id, series,key_type,date_added):
    try:
         new_m_key = MasterKey(masterkey_id,series,key_type,date_added)
         db.session.add(new_m_key)
         db.session.commit()
         return new_m_key
    except SQLAlchemyError:
        db.session.rollback()
        return None

def get_all_masterkeys(size,offset):
    m_offset = (offset * size)

    masterkeys = MasterKey.query.all()
    
    if not masterkeys:
        return {'num_pages': 1, "data":[]}
    
    length_masterkeys = len(masterkeys)
    if length_masterkeys == 0:
        num_pages = 1
    elif length_masterkeys%size != 0:
        num_pages  = int((length_masterkeys/size)+1)
    else:
        num_pages = int(length_masterkeys/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop > length_masterkeys):
        stop = length_masterkeys
    m_list = []

    for d in masterkeys[index:stop]:
        m_list.append(d.toJSON())
    return {'num_pages':num_pages, "data":m_list}
    

def get_masterkey_by_id(id):
    masterkey = MasterKey.filter(or_(MasterKey.id.like(id), MasterKey.masterkey_id.like(id))).first()

    if not masterkey:
        return None

    return masterkey

def update_series(id,new_series):
    masterkey = get_masterkey_by_id(id)

    if not masterkey:
        return None
    
    try:
        masterkey.series = new_series
        db.session.add(masterkey)
        db.session.commit()
        return masterkey
    except SQLAlchemyError:
        db.session.rollback()
        return None


def update_masterkey_id(id,new_id):
    masterkey = get_masterkey_by_id(id)

    if not masterkey:
        return None
    
    try:
        masterkey.masterkey_id = new_id
        db.session.add(masterkey)
        db.session.commit()
        return masterkey
    except SQLAlchemyError:
        db.session.rollback()
        return None

def delete_masterkey(id):
    masterkey =get_masterkey_by_id(id)

    if not masterkey:
        return None
    try:
        db.session.delete(masterkey)
        db.session.commit()
        return masterkey
    except SQLAlchemyError:
        db.session.rollback()
        return None