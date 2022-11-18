from database import db
from models import Rent
from sqlalchemy.exc import SQLAlchemyError

# create function to cal amount owed

def create_new_rental(student_id,locker_id,rent_type, rent_date_from, rent_date_to, date_returned,amount_owed):
    try:
        new_rent = Rent (student_id,locker_id,rent_type,rent_date_from,rent_date_to,date_returned,amount_owed)
        db.session.add(new_rent)
        db.session.commit()
        return new_rent
    except SQLAlchemyError:
        db.session.rollback()
        return []

def get_rent_by_id(id):
    rent = Rent.query.filter_by(id = id).first()

    if not rent:
        return []

    return rent

def get_rent_by_id_json(id):
    rent_json = get_rent_by_id(id)

    if not rent_json:
        return []
    return rent_json.toJSON()

def update_rental(id,student_id,locker_id,rent_type, rent_date_from, rent_date_to, date_returned,amount_owed):
    rent = get_rent_by_id(id)

    if not rent:
        return []

    if student_id != "":
        rent.student_id = student_id
    if locker_id != "":
        rent.locker_id = locker_id
    if rent_type != "":
        rent.rent_type = rent_type
    if rent_date_to != "":
        rent.rent_date_to = rent_date_to
    if rent_date_from != "":
        rent.rent_date_from = rent_date_from
    if date_returned != "":
        rent.date_returned = date_returned
    if amount_owed != "":
        rent.amount_owed = amount_owed
        
    try:
        db.session.add(rent)
        db.session.commit()
        return rent
    except SQLAlchemyError:
        db.session.rollback()
        return []
    
def delete_rent(id):
    rent = get_rent_by_id(id)

    if not rent:
        return []
    try:
        db.session.delete(rent)
        db.session.commit()
        return rent
    except SQLAlchemyError:
        db.session.rollback()
        return []

def get_all_rents():
    rents = Rent.query.all()

    if not rents:
        return []
    
    return [r.toJSON() for r in rents]
