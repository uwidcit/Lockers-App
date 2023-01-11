from models import RentTypes,Rent
from models.rentTypes import Types
from database import db
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

def new_rentType(period_from, period_to, type, price):
    try:
        rentType = RentTypes(period_from,period_to,type,price)
        db.session.add(rentType)
        db.session.commit()
        return rentType
    except SQLAlchemyError:
        db.session.rollback()
        return None

def get_rentType_by_id(id):
    rentType = RentTypes.query.filter_by(id = id).first()

    if not rentType:
        return None

    return rentType

def get_rentType_daily_period(period_from, period_to):
    rentType = RentTypes.query.filter(and_(RentTypes.period_to >= period_to, RentTypes.period_from <= period_from,RentTypes.type == Types.DAILY)).first()
     
    if not rentType:
        return None

    return rentType

def get_rentType_period(period_to):
    rentType = RentTypes.query.filter_by(period_to = period_to)

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]

def get_rentType_price(price):
    rentType = RentTypes.query.filter_by(price = price)

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]

def update_rentType_price(id,new_price):
    #first check to see if a rentType exist in rent
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        return []
    try:
        rentType = get_rentType_by_id(id)

        if not rentType:
            return None
        rentType.price = new_price
        db.session.add(rentType)
        db.session.commit()
        return rentType
    except SQLAlchemyError:
        db.session.rollback()
        return None

def update_rentType_period(id, period_from, period_to):
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        return []

    rent_type = get_rentType_by_id(id)

    if not rent_type:
        return None
    
    rent_type.period_from = period_from
    rent_type.period_to = period_to
    try:
        db.session.add(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError:
        db.session.rollback()
        return None

def update_rentType_type(id,type):
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        return []

    rent_type = get_rentType_by_id(id)

    if not rent_type:
        return []
    
    try:
        if type.upper() in Types.__members__:
            rent_type.type = Types[type.upper()]
            db.session.add(rent_type)
            db.session.commit()
            return rent_type
    except SQLAlchemyError:
        db.session.rollback()
        return []
        
def delete_rent_type(id):
    rent = Rent.query.filter_by(rent_type = id).first()
    
    if rent:
        return None

    rent_type = get_rentType_by_id(id)

    if not rent_type:
        return None
    try:
        db.session.delete(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError:
        db.session.rollback()
        return []    

def get_All_rentType():
    rentType = RentTypes.query.all()

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]

def get_rt_Type():
    return [rt.value for rt in Types]