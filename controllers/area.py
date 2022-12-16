from models import Area
from database import db

from sqlalchemy.exc import SQLAlchemyError

def add_new_area(locker_id, description, longitude,latitude):
    try:
        new_area = Area(locker_id,description,longitude,latitude)
        db.session.add(new_area)
        db.session.commit()
        return new_area
    except SQLAlchemyError:
        db.session.rollback()
        return []

def get_area_by_id(id):
    area = Area.query.filter_by(id = id).first()
    if not area: 
        return None
    return area

def get_area_by_locker(locker_id):
    area = Area.query.filter_by(locker_id = locker_id).first()
    if not area: 
        return None
    return area


def get_area_all():
    areas = Area.query.all()
    if not areas:
        return []
    return [a.toJSON() for a in areas]

