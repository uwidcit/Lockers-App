from App.models import MasterKey,Key
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from App.models.masterkey import Key_Type

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

def get_all_masterkeys_no_offset():
     masterkeys = MasterKey.query.all()

     if not masterkeys:
         return []
     return [m.masterkey_id for m in masterkeys]

    

def get_masterkey_by_id(id):
    if id == '' or id is None:
        return None 

    masterkey = MasterKey.query.filter(MasterKey.masterkey_id.contains(id)).first()

    if not masterkey:
        return None

    return masterkey

def update_series(id,new_series):
    masterkey = get_masterkey_by_id(id)

    if new_series is None or new_series == '':
        return None

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

def update_masterkey_type(id, new_type):
    if new_type is None:
        return None
    masterkey = get_masterkey_by_id(id)
    if not masterkey:
        return None
    
    try:
        if new_type.upper() in Key_Type.__members__:
            masterkey.key_type = Key_Type[new_type.upper()]
            db.session.add(masterkey)
            db.session.commit()
            return masterkey
    except SQLAlchemyError:
        db.session.rollback()
        return None

def search_masterkey(query,offset,size):
    if query is None or query == '':
        return None
    if query.upper() in Key_Type.__members__:
        data = db.session.query(MasterKey).filter(or_(MasterKey.key_type == Key_Type[query.upper()],MasterKey.masterkey_id.contains(query),MasterKey.series.contains(query))).all()
    else:
        data = db.session.query(MasterKey).filter(or_(MasterKey.masterkey_id.contains(query),MasterKey.series.contains(query))).all()

    if not data:
        return {'num_pages':1,'data':[]}
    
    length_mkey = len(data)
    if length_mkey == 0:
         num_pages = 1
    
    if length_mkey%size != 0:
        num_pages = int((length_mkey/size) + 1)
    else:
        num_pages = int(length_mkey/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop > length_mkey):
        stop = length_mkey
    
    m_list = []
    for masterkey in data[index:stop]:
        m_list.append(masterkey.toJSON())
    return {"num_pages": num_pages,"data":m_list}

def get_key_masterkey_offset(id,offset,size):
    data = db.session.query(MasterKey,Key).join(Key).filter_by(masterkey_id = id).all()
    if not data:
        return {'num_pages':1,'data':[],"num_keys":0}
    
    length_mkey = len(data)
    if length_mkey == 0:
         num_pages = 1
    
    if length_mkey%size != 0:
        num_pages = int((length_mkey/size) + 1)
    else:
        num_pages = int(length_mkey/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop >= length_mkey):
        stop = length_mkey
    
    m_list = []
    for masterkey,key in data[index:stop]:
        temp_key = key.toJSON()
        current_locker = temp_key['KeyHistory']['locker_id']
        if not current_locker:
            current_locker = ""
        temp_key['current_locker'] = current_locker
        m_list.append(temp_key)
    return {"num_pages": num_pages,"data":m_list,"num_keys":length_mkey}