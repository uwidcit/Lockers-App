from models import Key
from database import db
from sqlalchemy.exc import SQLAlchemyError

def add_new_key(key_id,key_1_status, key_2_status):
    try:
        new_key = Key(key_id,key_1_status,key_2_status)
        db.session.add(new_key)
        db.session.commit()
        return new_key
    except SQLAlchemyError:
        db.session.rollback()
        return []

def get_key_id(id):
    key = Key.query.filter_by(key_id = id).first()
    if not key:
        return []
    return key.toJSON()

def get_all_key_1s_available():
    keys = Key.query.filter_by(key_1_status = 'TRUE').all()
    if not keys:
        return []
    return [k.toJSON() for k in keys]

def get_all_key_2s_available():
    keys = Key.query.filter_by(key_2_status = 'TRUE').all()
    if not keys:
        return []
    return [k.toJSON() for k in keys]

def get_all_key_available():
    keys = Key.query.filter_by(key_1_status = 'TRUE', key_2_status = 'TRUE').all()
    if not keys:
        return []
    return [k.toJSON() for k in keys]

def get_all_key_unavailable():
    keys = Key.query.filter_by(key_1_status = 'FALSE', key_2_status = 'FALSE').all()
    if not keys:
        return []
    return [k.toJSON() for k in keys]

def get_all_keys():
    keys = Key.query.all()
    if not keys:
        return []
    return [k.toJSON() for k in keys]