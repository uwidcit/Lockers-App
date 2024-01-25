from App.models import Area
from App.database import db
from sqlalchemy import and_, or_, Sequence
from sqlalchemy.exc import SQLAlchemyError

def add_new_area(description, longitude, latitude):
    try:
        new_area = Area(description,longitude, latitude)
        db.session.add(new_area)
        db.session.commit()
        return new_area
    except SQLAlchemyError as e:
        db.session.rollback()
        raise("Unable to add new Area")

def restore_area(id,description, longitude, latitude):
    seq = Sequence(name='area_id_seq')
    try:
        new_area = Area(description,longitude, latitude)
        new_area.id = id
        db.session.add(new_area)
        db.session.execute(seq)
        db.session.commit()
        return new_area
    except SQLAlchemyError as e:
        db.session.rollback()
        raise("Unable to add new Area")
    

def get_area_by_id(id):
    area = Area.query.filter_by(id = id).first()
    if not area:
        raise("Area does not exist") 
    return area

def get_lockers_in_area(id):
    area = Area.query.filter_by(id = id).first()
    if not area:
        raise("Area does not exist")
    return area.getLockersInArea()


#marked
def get_area_by_description(description):
    areas = Area.query.filter(Area.description.contains(description)).all()
    if not areas:
        return None
    return areas

#marked
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
        db.session.rollback()
        raise("Unable to set description. Check Error Log for more Details")

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
        db.session.rollback()
        raise("Unable to set latitude. Check Error Log for more Details")
        

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
        db.session.rollback()
        raise("Unable to set longitude. Check Error Log for more Details")
        
        

def delete_area(id):
    area = get_area_by_id(id)
    if not area: 
        return None
    if area.locker:
        raise('Unable to delete area with lockers in it')
    
    try:
        db.session.delete(area)
        db.session.commit()
        return area
    except SQLAlchemyError as e:
        db.session.rollback()
        raise("Unable to delete Area. Check Error Log for more Details")
        
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

    if areas is None:
        return 0 
    else:
        return len(areas)

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
    try:
        int_query = int(query)
        data = Area.query.filter(or_(Area.id == int_query,Area.longitude == query, Area.latitude == query)).all()
    except:
        data = Area.query.filter(Area.description.contains(query)).all()

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
    areas = Area.query.filter(and_(Area.id != areaID1, Area.id != areaID2)).all()
    if not areas:
        return None
    return [a.getLockersInArea() for a in areas]