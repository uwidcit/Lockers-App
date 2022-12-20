from models import Rent, Status 
from controllers.lockers import rent_locker,get_locker_id,release_locker
from datetime import datetime
from database import db 
from sqlalchemy.exc import SQLAlchemyError

def create_rent(student_id, locker_id,rentType, rent_date_from, rent_date_to):
    if get_overdue_rent_by_student(student_id) or get_owed_rent_by_student(student_id):
        return []

    if get_locker_id(locker_id): 
        try:
            rent = Rent(student_id, locker_id, rentType,rent_date_from,rent_date_to)
            db.session.add(rent)
            db.session.commit()
            rent_locker(locker_id)
            
            return rent
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()   
            return None
        


def get_rent_by_id(id):
    rent = Rent.query.filter_by(id=id).first()

    if not rent:
        return None
   
    return rent

def update_rent(id):
    rent = get_rent_by_id(id)

    if not rent:
        return None
    
    rent.amount_owed = rent.cal_amount_owed()
    rent.status = rent.check_status()

    try:
        db.session.add(rent)
        db.session.commit()
        return rent

    except SQLAlchemyError:
        db.session.rollback()
        return None


def get_overdue_rent_by_student(s_id):
    rent = Rent.query.filter_by(student_id= s_id,status = Status.OVERDUE).first()
    if not rent :
        return None
    return rent

def get_owed_rent_by_student(s_id):
    rent = Rent.query.filter_by(student_id= s_id,status = Status.OWED).first()
    if not rent :
        return None
    return rent

def release_rental(id,d_returned):
    rent = get_rent_by_id(id)

    if not rent:
        return None
    rent.date_returned = d_returned
    rent.status = Status.RETURNED
    
    try:
        db.session.add(rent)
        db.session.commit()
        release_locker(rent.locker_id)
        return rent

    except SQLAlchemyError:
        db.session.rollback()
        return None

def get_all_rentals():
    rents = Rent.query.all()

    if not rents:
        return None

    return[r.toJSON() for r in rents]

    