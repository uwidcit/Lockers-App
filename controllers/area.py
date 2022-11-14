from models import Area
from database import db

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

def add_new_area(location):
    try:
        new_area = Area(location=location)
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
