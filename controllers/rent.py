from models import Rent, Status 
from controllers import (
    rent_locker,
    get_locker_id,
    get_rentType_by_id,
    get_rentType_daily_period,
    release_locker)
from datetime import datetime
from database import db 
from sqlalchemy.exc import SQLAlchemyError

def period_elapsed(rentType_id, date_returned, rent_date_from, rent_date_to):
    type = get_rentType_by_id(rentType_id)

    if not type:
        return -1

    if type.value == "Hourly":
        if date_returned:
            time = date_returned - rent_date_from 
            return time.timedelta.hours
        elif datetime.now() > rent_date_to:
            time = datetime.now() - rent_date_from 
            return time.timedelta.hours
        time = rent_date_to - rent_date_from   
        return  time.time.timedelta.hours
    elif type.value == "Daily":
        if date_returned:
            time = date_returned - rent_date_from 
            return time.days
        elif datetime.now() > rent_date_to:
            time = datetime.now() - rent_date_from 
            return time.days
        time = rent_date_to - rent_date_from   
        return  time.days
    elif type.value == "Weekly":
        if date_returned:
            time = date_returned - rent_date_from
            return time.days/7
        elif datetime.now() > rent_date_to:
            time = datetime.now() - rent_date_from 
            return time.days/7
        time = rent_date_to - rent_date_from   
        return time.days/7
        
    elif type.value == "Monthly":
        if date_returned:
            time = (date_returned.year - rent_date_from.year) * 12 + (date_returned.month - rent_date_from.month)
            return time
        elif datetime.now() > rent_date_to:
            time = time = (datetime.now().year - rent_date_from.year) * 12 + (datetime.now().month - rent_date_from.month)
            return time.timedelta.hours
        time = (rent_date_to.year - rent_date_from.year)  * 12 + (rent_date_to.month - rent_date_from.month)
        return  time
    elif type == "Semester":
        return 1

def cal_amount_owed(rentType_id, date_returned, rent_date_from, rent_date_to):
    type = get_rentType_by_id(rentType_id)

    if not type:
        return -1

    price = float(type.price)

    return (price * period_elapsed(rentType_id, date_returned, rent_date_from, rent_date_to) + late_fees(rentType_id, date_returned, rent_date_from, rent_date_to))
        
    
def late_fees(rentType_id, date_returned, rent_date_from, rent_date_to):
    type = get_rentType_by_id(rentType_id)
    
    if not type:
        return -1
    daily_price = get_rentType_daily_period()
    
    if not daily_price:
        daily_price = 1

    if type == "Hourly":
        timestamp = datetime.now()
        if timestamp > rent_date_to and not date_returned:
            time = timestamp - rent_date_to 
           
        elif date_returned and date_returned > rent_date_to:
            time  = rent_date_to - rent_date_from
        else:
            return 0.00
        return type.price * time.timedetlta.hours
        
    else:
        if datetime.now() > rent_date_to:
            time  = datetime.now - rent_date_to

        elif date_returned and date_returned > rent_date_to:
                time  = date_returned - rent_date_to
        else:
            return 0.0
        return daily_price.price * time

def create_rent(student_id, locker_id,rentType, rent_date_from, rent_date_to):
    if get_overdue_rent_by_student(student_id) or get_owed_rent_by_student(student_id):
        return []

    if get_locker_id(locker_id): 
        try:
            cal_amount_owed(rentType, type, None , rent_date_from, rent_date_to, cal_amount_owed(rentType,None,rent_date_from,rent_date_to))
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

    