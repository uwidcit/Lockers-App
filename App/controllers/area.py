from App.models import Area
from App.database import db
from flask import flash
from App.controllers.log import create_log
from datetime import datetime
from sqlalchemy import or_
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

def get_area_by_coordinates(long,lat):
    areas =Area.query.filter_by(longitude = long,latitude = lat)
    if not areas:
        return None
    return [a.toJSON() for a in areas]

def get_area_by_description(description):
    areas = Area.query.filter(Area.description.like(description)).all()
    if not areas:
        return None
    return areas

def get_area_by_description_toJSON(description):
    areas = get_area_by_description(description)
    if not areas:
        return None
    return [a.toJSON() for a in areas]


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
    areas = Area.query.all()

    count = 0
    
    for a in areas:
        count += 1

    if not count or count == 0:
        db.session.rollback()
        return 1
    return count

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

def search_area(query, offset,size):
    data = Area.query.filter(or_(Area.id.like(query), Area.description.like(query), Area.longitude.like(query), Area.latitude.like(query))).all()

    if not data:
        return None

    length_area = len(data)
    if length_area == 0:
         num_pages = 1
    
    if length_area%size != 0:
        num_pages = int((length_area/size) + 1)
    else:
        num_pages = int(length_area/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop > length_area):
        stop = length_area

    a_list = []
    for area in data[index:stop]:
        a_list.append(area.toJSON())
    return {"num_pages":num_pages,"data":a_list}

def return_lockers(id,size,offset):
    area = get_area_by_id(id)
    
    if not area:
        return None
    
    length_area = len(area.locker)
    if length_area == 0:
         num_pages = 1
    
    if length_area%size != 0:
        num_pages = int((length_area/size) + 1)
    else:
        num_pages = int(length_area/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop > length_area):
        stop = length_area
    
    a_list = []

    for d in area.locker[index:stop]:
        a_list.append(d.toJSON())

    return {"num_pages":num_pages,"data":a_list}
    
def get_area_all_except(areaID):
    areas = Area.query.filter(Area.id != areaID).all()
    if not areas:
        return None
    return [a.toJSON() for a in areas]

def get_lockers_all_except(areaID1, areaID2):
    areas = Area.query.filter(or_(Area.id != areaID1, Area.id != areaID2)).all()
    if not areas:
        return None
    return [a.getLockersInArea() for a in areas]