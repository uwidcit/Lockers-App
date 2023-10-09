from App.models import Rent,RentTypes,KeyHistory
from App.models.locker import Locker
from App.models.rent import RentStatus as Status, RentMethod as Method
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
    get_current_rental_c,
    not_verified
)

from App.controllers.student import update_student_status

from App.controllers.key_history import getKeyHistory
from App.controllers.log import create_log
from flask import flash
from datetime import datetime,timedelta
from App.database import db 
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

def period_elapsed(type, rent_date_from, rent_date_to):

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
        if time.days < 1:
            return 1   
        return  time.days
    else:
        return 1

def init_amount_owed(rentType_id, rent_date_from, rent_date_to):
    type = get_rentType_by_id(rentType_id)

    if not type:
        return -1

    price = float(type.price)

    return round((price * period_elapsed(type, rent_date_from, rent_date_to)),2)
        
def recal_amount_owed(rent,rentType_id,date_returned,rent_date_from,rent_date_to):
    timestamp = datetime.now()
    semester_period = get_rentType_by_id(rentType_id)
    orignal_duration = period_elapsed(semester_period,rent_date_from,rent_date_to)

    if date_returned:
        date_returned_1 = date_returned
        return_duration = period_elapsed(semester_period,rent_date_from,date_returned)
    else:
        date_returned_1 = timestamp
        return_duration = period_elapsed(semester_period,rent_date_from,timestamp)

    
    if date_returned_1.date() <= semester_period.period_to:
        if return_duration > orignal_duration:
            rent.late_fees = late_fees(semester_period, return_duration, orignal_duration)
            return rent
        else:
            return rent
    else:
        rent.late_fees = late_fees(semester_period, return_duration, orignal_duration)
        return rent   

def late_fees(type, duration, original_duration):
    
    timestamp = datetime.now()
    if not type:
        return -1
    
    return (duration - original_duration) * type.price

def cal_fixed_price(rentType_id):
    type = get_rentType_by_id(rentType_id)

    if not type:
        return -1

    return float(type.price)

def create_rent(student_id, locker_id,rentType, rent_date_from, rent_date_to,rent_method,date_returned):
    locker = get_locker_id(locker_id)
    if get_rentType_by_id(rentType) is None:
        raise Exception('Rent Type does not exist')
    if locker:
        if locker[0].status.value != "Free":
            raise Exception('Locker is already rented')
        try:
            locker_instance = get_current_locker_instance(locker_id)
            if locker_instance:
                if rent_method.upper() == "FIXED":
                    amount_owed = cal_fixed_price(rentType)
                elif rent_method.upper() == "RATE":
                    amount_owed = init_amount_owed(rentType, rent_date_from, rent_date_to)
                else:
                    return None
                rent = Rent(student_id, locker_instance.id, rentType,rent_date_from,rent_date_to,amount_owed,rent_method,date_returned)
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
        
def import_verified_rent(student_id,locker_id,rentType,rent_date_from,rent_date_to,amount_owed,status,date_returned,rent_method):
    locker_instance = get_current_locker_instance(locker_id)
    rent = Rent(student_id, locker_instance.id, rentType,rent_date_from,rent_date_to,amount_owed,rent_method)
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

def swap_rent(old_locker,new_locker,rentType, rent_date_from, rent_date_to,rent_method,date_returned):
    rent = get_current_rental_c(old_locker)
    if not rent:
        raise Exception("Rent doesn't exist")
    locker = get_locker_id(new_locker)
    original_locker = rent.keyHistory_id
    if locker[0].status.value != "Free":
        raise Exception('Locker is already rented')
    locker_instance = get_current_locker_instance(new_locker)

    rent.keyHistory_id = locker_instance.id
    rent.rent_type = rentType
    rent.rent_date_from = rent_date_from
    rent.rent_date_to = rent_date_to
    if rent_method.upper() == "FIXED":
        rent.amount_owed = cal_fixed_price(rentType)
    elif rent_method.upper() == "RATE":
        rent.amount_owed = init_amount_owed(rentType, rent_date_from, rent_date_to)
    else:
        raise Exception ("Invalid Rent Method")
    if date_returned:
        rent.date_returned = date_returned
    try:
        db.session.add(rent)
        db.session.commit()
        release_locker(original_locker)
        rent_locker(new_locker)
        return rent
    except:
        db.session.rollback()
        return None

def get_rent_by_id(id):
    rent = Rent.query.filter_by(id=id).first()

    if not rent:
        flash("Rent does not exist")
        return None
    
    return rent

def rent_additional_payments(id,monetary_value):
    rent = update_rent(id)

    if not rent:
        raise Exception("Rent doesn't exist")
    
    rent.cal_additional_fees(monetary_value)
    try:
        db.session.add(rent)
        db.session.commit()
    except:
        db.session.rollback()
        return None

def update_rent(id):
    rent = get_rent_by_id(id)

    if rent is None:
        return None
    
    if rent.status is Status.VERIFIED:
        return rent
         
    #if rent.rent_method == Method.RATE:
        #rent = recal_amount_owed(rent,rent.rent_type,rent.date_returned,rent.rent_date_from,rent.rent_date_to)
    
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

def get_all_rentals_active():
    rents = db.session.query(Rent,KeyHistory,Locker,RentTypes).filter(Rent.status != Status.VERIFIED,KeyHistory.id == Rent.keyHistory_id, RentTypes.id == Rent.rent_type, Locker.locker_code == KeyHistory.locker_id).all()
    date = datetime.now()
    if not rents:
        return []

    data = []
    for r,kh,l,rt in rents:
        if date > r.rent_date_to:
            d = update_rent(r.id).toJSON()
        else:
            d = r.toJSON()
        d['key'] = kh.key_id
        d['locker_code'] = kh.locker_id
        d['rent_types'] = rt.type.value
        d['rent_size'] = l.locker_type.value
        data.append(d)

    return data

def get_all_rentals_inactive():
    rents = db.session.query(Rent,KeyHistory,RentTypes).filter(Rent.status == Status.VERIFIED,KeyHistory.id == Rent.keyHistory_id, RentTypes.id == Rent.rent_type).all()
    date = datetime.now()
    if not rents:
        return []

    data = []
    for r,kh,rt in rents:
        if date > r.rent_date_to:
            d = update_rent(r.id).toJSON()
        else:
            d = r.toJSON()
        d['key'] = kh.key_id
        d['locker_code'] = kh.locker_id
        d['rent_types'] = rt.type.value
        data.append(d)

    return data
def update_rent_values(id,rent_type,rent_method,rent_date_from,rent_date_to,date_returned,late_fees,additional_fees):
    rent = update_rent(id)
    if rent:
        if rent.rent_date_from != rent_date_from:
            rent.rent_date_from = rent_date_from
        
        if rent.rent_date_to != rent_date_to:
            rent.rent_date_to = rent_date_to
        
        if rent.rent_method.value.upper() != rent_method:
             if rent_method.upper() in Method.__members__:
                 rent.rent_method = Method[rent_method.upper()]
        if rent.rent_type != rent_type:
            rent.rent_type = rent_type
        rent.amount_owed = init_amount_owed(rent_type,rent.rent_date_from,rent.rent_date_to)
        rent.date_returned = date_returned
        rent.late_fees = late_fees
        rent.additional_fees = additional_fees
        try:
            db.session.add(rent)
            db.session.commit()
            return rent
        except Exception as e:
            db.session.rollback()
            return None


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
    
    


    
