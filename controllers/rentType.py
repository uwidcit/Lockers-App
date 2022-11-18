from database import db
from models import RentTypes
from sqlalchemy.exc import SQLAlchemyError

def create_new_rent_type(period,type,price):
    try:
        new_rent_type = RentTypes(period,type,price)
        db.session.add(new_rent_type)
        db.session.commit()
        return new_rent_type
    except SQLAlchemyError:
        db.session.rollback()
        return []

def get_rent_type_by_id(id):
    rent_type = RentTypes.query.filter_by(id=id).first()

    if not rent_type:
        return []

    return rent_type

def rent_type_toJSON(id):
    rent_type_json = get_rent_type_by_id(id)

    if not rent_type_json:
        return []

    return rent_type_json.toJSON()

def update_rent_type(id, period,type,price):
    #Write some code to check if a rent record exist with this id before updating it

    rent_type = get_rent_type_by_id(id)

    if not rent_type:
        return []
    
    if period !="":
        rent_type.period = period
    if type != "":
        rent_type.type = type
    if price !="":
        rent_type.price = price
    try:
        db.session.add(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError:
        db.session.rollback()
        return []

def delete_rent_type():
    rent_type = get_rent_type_by_id(id)

    if not rent_type:
        return []
    try:
        db.session.delete(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError:
        db.session.rollback()
        return []

def get_all_rent_types():
    rent_types = RentTypes.query.all()

    if not rent_types:
        return []

    return [r.toJSON() for r in rent_types]
