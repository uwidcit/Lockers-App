from App.models import Key
from App.models.key import Key_Status
from App.database import db
from sqlalchemy.exc import SQLAlchemyError



def new_key(key_id, masterkey_id,key_status,date_added):
    try:
         new_key = Key(key_id,masterkey_id,key_status,date_added)
         db.session.add(new_key)
         db.session.commit()
         return new_key
    except SQLAlchemyError:
        db.session.rollback()
        return None

def get_all_keys(size,offset):
    k_offset = (offset * size)

    keys = Key.query.all()

    if not keys:
        return {'num_pages':1, "data":[]}
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
    
    

def get_key_by_id(id):
    key = Key.query.filter(Key.key_id.contains(id)).first()

    if not key:
        return None

    return key

def update_key_id(id,new_key_id):
    key = get_key_by_id(id)

    if not key:
        return None
    
    try:
        key.key_id = new_key_id
        db.session.add(key)
        db.session.commit()
        return key
    except SQLAlchemyError:
        db.session.rollback()
        return None


def update_key_masterkey_id(id,new_id):
    key = get_key_by_id(id)

    if not key:
        return None
    
    try:
        key.masterkey_id = new_id
        db.session.add(key)
        db.session.commit()
        return Key
    except SQLAlchemyError:
        db.session.rollback()
        return None

def update_key_status(id,new_status):
    key = get_key_by_id(id)

    if not key:
        return None
    
    try:
        if new_status.upper() in Key_Status.__members__:
            key.key_status = Key_Status[new_status.upper()]
        db.session.add(key)
        db.session.commit()
        return key
    except SQLAlchemyError:
        db.session.rollback()
        return None

def delete_key(id):
    key =get_key_by_id(id)

    if not key:
        return None
    try:
        db.session.delete(key)
        db.session.commit()
        return key
    except SQLAlchemyError:
        db.session.rollback()
        return None
def get_key_statuses():
    return [e.value for e in Key_Status]

def get_all_keys_id():
    keys = Key.query.all()

    if not keys:
        return []
    return [k.key_id for k in keys]