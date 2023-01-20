from models import Locker
from models.locker import Status, LockerTypes,Key
from database import db
from controllers.log import create_log
from datetime import datetime
from flask import flash
from sqlalchemy import or_,and_
from sqlalchemy.exc import SQLAlchemyError

def add_new_locker(locker_code,locker_type,status,key,area,):
    try:
        locker = Locker(locker_code,locker_type,status,key,area)
        db.session.add(locker)
        db.session.commit()
        return locker
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(create_log(e, locker_code))
        return None

def get_lockers_available():
    locker_list = Locker.query.filter(and_(Locker.status == Status.FREE)).all()
    if not locker_list:
        return []
    return [l.toJSON() for l in locker_list]

def get_locker_id(id):
    locker = Locker.query.filter_by(locker_code = id).first()
    if not locker:
        return None
    return locker

def get_all_lockers():
    locker_list = Locker.query.all()
    if not locker_list:
        return []
    return [l.toJSON() for l in locker_list]

def get_num_lockers():
    try:
        lockers = Locker.query.all()
        count = 0

        for l in lockers:
            count += 1

        if not count or count == 0:
            return 1
        return count
    except:
        db.session.close()
        db.session.begin()

def get_num_locker_page(size):
    count = get_num_lockers()

    if count == 0:
        return 1

    if count%size != 0:
        return int(count/size + 1)

    return int(count/size)

def get_lockers_by_offset(size,offset):
     l_offset = (offset * size) - size
     lockers = Locker.query.limit(size).offset(l_offset)

     if not lockers:
        return None
     return [l.toJSON() for l in lockers]

def rent_locker(id):
    locker = get_locker_id(id)
    if not locker or locker.status == Status.RENTED:
        flash("locker already Rented")
        return None
    locker.status = Status.RENTED
    try:
        db.session.add(locker)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to Rent Locker. Check Error Log for more Details")
        db.session.rollback()
        return None

def not_verified(id):
    locker = get_locker_id(id)
    
    if not locker :
        return None
    
    locker.status = Status.NVERIFIED
    
    try:
        db.session.add(locker)
        db.session.commit()
        
        return locker
    except SQLAlchemyError as e:
        db.session.rollback()
        create_log(id, type(e), datetime.now())
        flash("Unable to release Locker. Check Error Log for more Details")
        return None

def release_locker(id):
    locker = get_locker_id(id)
    
    if not locker :
        return None
    
    locker.status = Status.FREE
    
    try:
        db.session.add(locker)
        db.session.commit()
        
        return locker
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to release Locker. Check Error Log for more Details")
        db.session.rollback()
        return None

def delete_locker(id):
    locker = get_locker_id(id)
    if not locker:
        return None
    try:
        db.session.delete(locker)
        db.session.commit()
        return locker
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to delete Locker. Check Error Log for more Details")
        db.session.rollback()
        return None
    
def update_key(id, new_key):
    locker = get_locker_id(id)
    if not locker:
        return None
    try:
         if new_key.upper() in Key.__members__:
            locker.key = Key[new_key.upper()]
            db.session.add(locker)
            db.session.commit()
            return locker
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to update key. Check Error Log for more Details")
        db.session.rollback()
        return None

def update_locker_status(id, new_status):
    locker = get_locker_id(id)
    if not locker:
        return None
    try:
        if new_status.upper() in Status.__members__:
            locker.status = Status[new_status.upper()]
            db.session.add(locker)
            db.session.commit()
            return locker
    except SQLAlchemyError:
        db.session.rollback()
        return None

def update_locker_type(id, new_type):
    locker = get_locker_id(id)
    if not locker:
        return None
    try:
        if new_type.upper() in LockerTypes.__members__:
            locker.locker_type = LockerTypes[new_type.upper()]
            db.session.add(locker)
            db.session.commit()
            return locker
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e.__dict__)
        create_log(id, type(e), datetime.now())
        flash("Unable to update locker status. Check Error Log for more Details")
        return None


def getStatuses():
    return [ e.value for e in Status ]

def getLockerTypes():
    return [ e.value for e in LockerTypes]
    
def getKey():
    return [ e.value for e in Key]