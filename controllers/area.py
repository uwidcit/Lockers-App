from models import Area
from database import db
from flask import flash
from controllers.log import create_log
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

def add_new_area(description, longitude, latitude):
    try:
        new_area = Area(description,longitude, latitude)
        db.session.add(new_area)
        db.session.commit()
        return new_area
    except SQLAlchemyError as e:
        flash("Unable to add new Area")
        db.session.rollback()
        return None

def get_area_by_id(id):
    area = Area.query.filter_by(id = id).first()
    if not area:
        flash("Area does not exist") 
        return None
    return area

def get_lockers_in_area(id):
    area = Area.query.filter_by(id = id).first()
    if not area:
        flash("Area does not exist")
        return None
    return area.getLockersInArea()

def set_description(id,new_description):
    area = get_area_by_id(id)
    if not area: 
        return None
    try:
        area.description = new_description
        db.session.add(area)
        db.session.commit()
        return area
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to set description. Check Error Log for more Details")
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
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to set latitude. Check Error Log for more Details")
        db.session.rollback()
        return None

def set_longitude(id,new_longitude):
    area = get_area_by_id(id)
    if not area: 
        return None
    try:
        area.longitude = new_longitude
        db.session.add(area)
        db.session.commit()
        return area
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to set longitude. Check Error Log for more Details")
        db.session.rollback()
        return None

def delete_area(id):
    area = get_area_by_id(id)
    if not area: 
        return None
    if area.locker:
        flash('Unable to delete area with lockers in it')
        return None
    try:
        db.session.delete(area)
        db.session.commit()
        return area
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to delete Area. Check Error Log for more Details")
        db.session.rollback()
        return None
def get_area_choices():
    areas = Area.query.with_entities(Area.id, Area.description).all()

    if not areas:
        return None
    
    return [(a.id,a.description) for a in areas]

def get_area_all():
    areas = Area.query.all()
    if not areas:
        return []
    return [a.toJSON() for a in areas]

def get_num_areas():
    return Area.query.count()

def get_num_area_page(size):
    count = get_num_areas()

    if count == 0:
        return 1

    if count%size != 0:
        return int(count/size + 1)

    return int(count/size)

def get_area_by_offset(size,offset):
     a_offset = (offset * size) - size
     areas = Area.query.limit(size).offset(a_offset)

     if not areas:
        return None
     return [a.toJSON() for a in areas]