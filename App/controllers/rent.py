from App.models import Rent 
from App.models.rent import RentStatus as Status
from math import ceil,floor

from App.controllers.rentType import (
    get_rentType_by_id,
    get_rentType_daily_period,
    )


from App.controllers.lockers import(
    get_locker_id,
    rent_locker,
    release_locker,
    get_current_locker_instance,
    not_verified
)

from App.controllers.student import update_student_status

from App.controllers.transactionLog import cal_transaction_amount
from App.controllers.log import create_log
from flask import flash
from datetime import datetime,timedelta
from App.database import db 
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

def period_elapsed(rentType_id, rent_date_from, rent_date_to):
    type = get_rentType_by_id(rentType_id)

    if not type:
        return -1

    if type.type.value == "Hourly":
        time = rent_date_to - rent_date_from
        period = floor((time.days*24) +  time.seconds/3600)
        if period == 0:
            period = 1
        return period
    elif type.type.value == "Daily":
        time = rent_date_to - rent_date_from   
        return  time.days
    elif type.type.value == "Weekly":
        time = rent_date_to - rent_date_from   
        return ceil(time.days/7)
    elif type.type.value == "Monthly":
        time = (rent_date_to.year - rent_date_from.year)  * 12 + (rent_date_to.month - rent_date_from.month)
        if time == 0 or time == -1:
            time = 1
        return ceil(time)
    elif type.type.value == "Semester":
        return 1

def init_amount_owed(rentType_id, rent_date_from, rent_date_to):
    type = get_rentType_by_id(rentType_id)

    if not type:
        return -1

    price = float(type.price)

    return round((price * period_elapsed(rentType_id, rent_date_from, rent_date_to)),2)
        
def recal_amount_owed(rentType_id,date_returned,rent_date_from,rent_date_to):
    timestamp = datetime.now()
    semester_period = get_rentType_by_id(rentType_id)
    orignal_duration = period_elapsed(rentType_id,rent_date_from,rent_date_to)

    if date_returned:
        date_returned_1 = date_returned
        return_duration = period_elapsed(rentType_id,rent_date_from,date_returned)
    else:
        date_returned_1 = timestamp
        return_duration = period_elapsed(rentType_id,rent_date_from,timestamp)

    
    if date_returned_1.date() <= semester_period.period_to:
        if return_duration > orignal_duration:
            return init_amount_owed(rentType_id,rent_date_from,rent_date_to) + late_fees(rentType_id,date_returned,rent_date_from,rent_date_to)
        else:
            return init_amount_owed(rentType_id,rent_date_from,rent_date_to)
    else:
        return init_amount_owed(rentType_id,rent_date_from,rent_date_to) + late_fees(rentType_id,semester_period.period_to,rent_date_from,rent_date_to)
   

def late_fees(rentType_id, date_returned, rent_date_from, rent_date_to):
    type = get_rentType_by_id(rentType_id)
    
    timestamp = datetime.now()
    if not type:
        return -1
    orignal_duration = period_elapsed(rentType_id,rent_date_from,rent_date_to)

    if date_returned:
        provisional_date = date_returned
        duration = period_elapsed(rentType_id,rent_date_from,date_returned)
    else:
        provisional_date = timestamp
        duration = period_elapsed(rentType_id,rent_date_from,timestamp)

    if duration > orignal_duration:
        return (duration - orignal_duration) * type.price
    else:
        return 0.00

def create_rent(student_id, locker_id,rentType, rent_date_from, rent_date_to):
    if get_overdue_rent_by_student(student_id) or get_owed_rent_by_student(student_id):
        flash("Unable to create rent. Rent Owed")
        return []
    locker = get_locker_id(locker_id)
    if locker: 
        try:
            locker_instance = get_current_locker_instance(locker_id)
            if locker_instance:
                amount_owed = init_amount_owed(rentType, rent_date_from, rent_date_to)
                rent = Rent(student_id, locker_instance.id, rentType,rent_date_from,rent_date_to,amount_owed)
                db.session.add(rent)
                db.session.commit()
                rent_locker(locker_id)
                update_student_status(student_id,"RENTING")
                return rent
            return None
        except SQLAlchemyError as e:
            print(e)
            create_log(student_id, type(e), datetime.now())
            flash("Unable to create rent. Check Error Log for more Details")
            db.session.rollback()   
            return None
        
def import_verified_rent(student_id,locker_id,rentType,rent_date_from,rent_date_to,amount_owed,status,date_returned):
    locker_instance = get_current_locker_instance(locker_id)
    rent = Rent(student_id, locker_instance.id, rentType,rent_date_from,rent_date_to,amount_owed)
    if status == 'Verified':
        rent.status = Status.VERIFIED
        rent.date_returned = date_returned
        try:
            db.session.add(rent)
            db.session.commit()
            return rent
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()   
            return None
    else:
        return None
    

def get_rent_by_id(id):
    rent = Rent.query.filter_by(id=id).first()

    if not rent:
        flash("Rent does not exist")
        return None
    
    return rent

def update_rent(id):
    rent = get_rent_by_id(id)

    if not rent:
        return None
    
    if rent.status is Status.VERIFIED:
        return rent
    
    amt = round(recal_amount_owed(rent.rent_type,rent.date_returned,rent.rent_date_from,rent.rent_date_to),2)
    if amt is not None:
        rent.amount_owed = round(round(amt,2) - round(cal_transaction_amount(id),2),2)
    rent.status = rent.check_status()

    if rent.status.value == "Overdue":
        update_student_status(rent.student_id,"OVERDUE")

    if rent.date_returned and rent.amount_owed > 0:
        update_student_status(rent.student_id,"OWED")
    
    if rent.date_returned and rent.amount_owed == 0:
        update_student_status(rent.student_id,"GOOD")

    try:
        db.session.add(rent)
        db.session.commit()
        return rent

    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to create rent. Check Error Log for more Details")
        db.session.rollback()
        return None


def get_overdue_rent_by_student(s_id):
    rent = Rent.query.filter(and_(Rent.student_id == s_id,Rent.status == Status.OVERDUE)).first()
    if not rent :
        return None
    rent = update_rent(rent.id)
    return rent

def get_owed_rent_by_student(s_id):
    rent = Rent.query.filter(and_(Rent.student_id== s_id,Rent.status == Status.OWED)).first()
    if not rent :
        return None
    rent = update_rent(rent.id)
    return rent

def get_student_current_rental(s_id):
    rent = Rent.query.filter(and_(Rent.student_id == s_id, Rent.status != Status.RETURNED, Rent.status != Status.VERIFIED)).first()

    if not rent:
        return None
    rent = update_rent(rent.id)
    return rent

def get_student_current_rental_toJSON(s_id):
    rent = get_student_current_rental(s_id)

    if not rent:
        return None

    return rent.toJSON()


def release_rental(id,d_returned):
    rent = update_rent(id)

    if not rent:
        return None

    if rent.status == Status.RETURNED or rent.status == Status.VERIFIED:
        return None
    
    try:
        rent.date_returned = d_returned
        rent.status = Status.RETURNED
        not_verified(rent.keyHistory_id)
        db.session.add(rent)
        db.session.commit()
        return rent

    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to release Rental. Check Error Log for more Details")
        db.session.rollback()
        return None

def verify_rental(id):
    rent = update_rent(id)
    
    if not rent:
        return None
    
    if rent.status != Status.RETURNED or rent.status == Status.VERIFIED:
        return None
    
    try:
        rent.status = Status.VERIFIED
        db.session.add(rent)
        db.session.commit()
        release_locker(rent.keyHistory_id)
        update_student_status(rent.student_id,"GOOD")
        return rent
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to verify Rental. Check Error Log for more Details")
        db.session.rollback()
        return None
        
def get_all_rentals():
    rents = Rent.query.all()

    if not rents:
        return None

    data = []
    for r in rents:
        data.append(update_rent(r.id).toJSON())

    return data

def get_transactions(id,size,offset):
    data = update_rent(id)
    
    if not data:
        return None
    
    length_trans = len(data.Transactions)
    if length_trans == 0:
         num_pages = 1
    
    if length_trans%size != 0:
        num_pages = int((length_trans/size) + 1)
    else:
        num_pages = int(length_trans/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop > length_trans):
        stop = length_trans
    
    s_list = []

    for d in data.Transactions[index:stop]:
        s_list.append(d.toJSON())

    return {"num_pages":num_pages,"data":s_list}

def get_rents_range(start_date, end_date):
    rent_query = db.session.query(Rent).filter(and_(Rent.rent_date_from >= start_date, Rent.rent_date_from < end_date)).all()
    if not rent_query:
        return 0
    data = [r.toJSON() for r in rent_query]
    return {"length":len(rent_query),"data":data}

def get_rents_returned_range(start_date, end_date):
    rent_query = db.session.query(Rent).filter(and_(Rent.rent_date_from >= start_date, Rent.rent_date_from < end_date,Rent.status == Status.VERIFIED)).all()
    if not rent_query:
        return 0
    data = [r.toJSON() for r in rent_query]
    return {"length":len(rent_query),"data":data}
    
    


    