from models import Rent, Status 
from controllers.rentType import get_rentType_by_id
from datetime import datetime
from database import db 
from sqlalchemy.exc import SQLAlchemyError

def create_rent(student_id, locker_id,rentType, rent_date_from, rent_date_to, date_returned):
    if get_overdue_rent_by_student(student_id) or get_owed_rent_by_student(student_id):
        return []
    try:
        amount_owed= calculate_amount_owed(rentType, rent_date_from, rent_date_to)
        rent = Rent(student_id, locker_id, rentType,rent_date_from,rent_date_to,date_returned,amount_owed,status=Status.LOAN)
        db.session.add(rent)
        db.session.commit()
        return rent
    except SQLAlchemyError:
        db.session.rollback()   
        return None

    
def calculate_amount_owed(rentType, rent_date_from, rent_date_to):
    type = get_rentType_by_id(rentType)
    if not type:
        return None
    
    return type.price * (rent_date_to - rent_date_from)

def calculate_late_fees(rentType, rent_date_to, date_returned):
    type = get_rentType_by_id(rentType)
    if not type:
        return None
    
    return type.price * (date_returned - rent_date_to)

def get_rent_by_id(id):
    rent = Rent.query.filter_by(id=id).first()

    if not rent:
        return None
    if datetime.now() > rent.rent_date_to:
        rent.amount_owed = rent.amount_owed + calculate_late_fees(rent.rentType,rent.rent_date_to,datetime.now())
    return rent

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

def release_rental(id,date_returned):
    rent = get_rent_by_id(id)

    if not rent:
        return None
    
    if date_returned > rent.rent_date_to:
        rent.amount_owed = rent.amount_owed + calculate_late_fees(rent.rentType, rent.rent_date_to, date_returned)

    elif date_returned < rent.rent_date_to and date_returned >= rent.rent_date_from:
        rent.amount_owed = calculate_amount_owed(rent.rent_type,rent.rent_date_from, date_returned)

    rent.status = Status.PAID

    try:
        db.session.add(rent)
        db.session.commit()
        return rent

    except SQLAlchemyError:
        db.session.rollback()
        return None

def get_all_rentals():
    rents = Rent.query.all()

    if not rents:
        return None
    
    for r in rents:
         if datetime.now() > r.rent_date_to:
            r.amount_owed = r.amount_owed + calculate_late_fees(r.rentType,r.rent_date_to,datetime.now())

    return[r.toJSON() for r in rents]