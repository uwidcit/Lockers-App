from models import LockerTypes
from database import db
from sqlalchemy.exc import SQLAlchemyError

def add_new_locker_type(locker_type, price):
    try:
        new_locker_type = LockerTypes(locker_type,price)
        db.session.add(new_locker_type)
        db.session.commit()
        return new_locker_type
    except SQLAlchemyError:
        db.session.rollback()
        return []
        
def get_all_locker_types():
    lockers = LockerTypes.query.all() 
    if not lockers:
        return []
    return [l.toJSON() for l in lockers]
