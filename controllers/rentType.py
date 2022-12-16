from models import RentType,Rent
from database import db
from sqlalchemy.exc import SQLAlchemyError


def new_rentType(period, type, price):
    try:
        rentType = RentType(period,type,price)
        db.session.add(rentType)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return None

def get_rentType_by_id(id):
    rentType = RentType.query.filter_by(id = id).first()

    if not rentType:
        return None

    return rentType



def get_rentType_period(period):
    rentType = RentType.query.filter_by(period = period)

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]

def get_rentType_price(price):
    rentType = RentType.query.filter_by(price = price)

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
    except SQLAlchemyError:
        db.session.rollback()
        return None

def update_rentType_period(id, period):
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        return []

    rent_type = get_rentType_by_id(id)

    if not rent_type:
        return []
    
    rent_type.period = period
    try:
        db.session.add(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError:
        db.session.rollback()
        return []

def update_rentType_type(id,type):
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        return []

    rent_type = get_rentType_by_id(id)

    if not rent_type:
        return []
    
    rent_type.type = type
    try:
        db.session.add(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError:
        db.session.rollback()
        return []
        
def delete_rent_type():
    rent = Rent.query.filter_by(rent_type = id).first()
    
    if rent:
        return []

    rent_type = get_rentType_by_id(id)

    if not rent_type:
        return []
    try:
        db.session.delete(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError:
        db.session.rollback()
        return []    
