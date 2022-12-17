from models import Area
from database import db

from sqlalchemy.exc import SQLAlchemyError

def add_new_area(locker_id, description, longitude, latitude):
    try:
        new_area = Area(description,locker_id,longitude, latitude)
        db.session.add(new_area)
        db.session.commit()
        return new_area
    except SQLAlchemyError:
        db.session.rollback()
        return None

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

def set_description(id,new_description):
    area = get_area_by_id(id)
    if not area: 
        return None
    try:
        area.description = new_description
        db.session.add(area)
        db.session.commit()
        return area
    except SQLAlchemyError:
        db.session.rollback()
        return None

def set_latitude(id, new_latitude):
    area = get_area_by_id(id)
    if not area: 
        return None
    try:
        area.latitude = new_latitude
        db.session.add(area)
        db.session.commit()
        return area
    except SQLAlchemyError:
        db.session.rollback()
        return None
    return

def set_longitude(id,new_longitude):
    area = get_area_by_id(id)
    if not area: 
        return None
    try:
        area.longitude = new_longitude
        db.session.add(area)
        db.session.commit()
        return area
    except SQLAlchemyError:
        db.session.rollback()
        return None
    return

def delete_area(id):
    area = get_area_by_id(id)
    if not area: 
        return None
    try:
        db.session.delete(area)
        db.session.commit()
        return area
    except SQLAlchemyError:
        db.session.rollback()
        return None
    return

def get_area_all():
    areas = Area.query.all()
    if not areas:
        return []
    return [a.toJSON() for a in areas]

