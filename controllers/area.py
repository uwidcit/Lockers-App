from models import Area
from database import db

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

def add_new_area(locker_id, description, longitude, latitude):
    try:
        new_area = Area(description,locker_id,longitude, latitude)
        db.session.add(new_area)
        db.session.commit()
        return new_area
    except SQLAlchemyError:
        db.session.rollback()
        return []

def get_area_all():
    areas = Area.query.all()
    if not areas:
        return []
    return [a.toJSON() for a in areas]
