from App.models import Locker
from App.models import Area, Rent, KeyHistory
from App.models.rent import RentStatus as RStatus
from App.models.locker import LockerStatus as Status, LockerTypes
from App.database import db
from App.controllers.log import create_log
from App.controllers.area import get_area_by_id,get_area_by_description
from App.controllers.key_history import new_keyHistory
from datetime import datetime
from flask import flash
from sqlalchemy import or_,and_
from sqlalchemy.exc import SQLAlchemyError

def add_new_locker(locker_code,locker_type,status,key_id,area):
    try:
        locker = Locker(locker_code,locker_type,status,area)
        db.session.add(locker)
        db.session.commit()
        new_keyHistory(key_id,locker.locker_code,datetime.now().date())
        print(locker.toJSON())
        return locker
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        flash(create_log(e, locker_code))
        return None

def get_lockers_available():
    locker_list = Locker.query.filter(Locker.status == Status.FREE).all()
    if not locker_list:
        return []
    return [l.toJSON() for l in locker_list]

def get_lockers_by_Status(status):
    if status.upper() in Status.__members__:
        locker_list = Locker.query.filter(Locker.status == Status[status.upper()]).all()
        if not locker_list:
            return None
        return [l.toJSON() for l in locker_list]
    return None

def get_locker_by_type(l_type):
    if l_type.upper() in LockerTypes.__members__:
        locker_list = Locker.query.filter(Locker.locker_type == LockerTypes[l_type.upper()]).all()
        if not locker_list:
            return None
        return [l.toJSON() for l in locker_list]
    return None

def get_locker_by_area_id(id):
    area = get_area_by_id(id)

    if not area:
        return None

    lockers = Locker.query.filter_by(area = id).all()

    if not lockers:
        return None
    return lockers

def get_locker_by_area_id_toJSON(id):
    lockers = get_locker_by_area_id(id)

    if not lockers:
        return {}
    return [l.toJSON() for l in lockers]


def get_lockers_by_area_description(description):
    area = get_area_by_description(description)
    
    lockers = []

    if not area:
        return None
    for a in area:
        lockers = lockers + get_locker_by_area_id_toJSON(a.id)
    return lockers


def get_locker_id(id):
    locker = db.session.query(Locker,Area).join(Area).filter(Locker.locker_code == id).first()
    if not locker:
        return None
    
    return locker

def get_locker_id_locker(id):
    locker = db.session.query(Locker).filter(Locker.locker_code == id).first()
    if not locker:
        return None
    return locker

def search_lockers(query,offset,size):
    data = db.session.query(Locker,Area).join(Area).filter(or_(Locker.locker_code.like(query), Locker.locker_type.like(query), Locker.status.like(query), Locker.status.like(query), Locker.key.like(query),Area.description.like(query))).all()

    if not data:
        return None
    length_lockers = len(data)
    if length_lockers == 0:
         num_pages = 1
    
    if length_lockers%size != 0:
        num_pages = int((length_lockers/size) + 1)
    else:
        num_pages = int(length_lockers/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop > length_lockers):
        stop = length_lockers
    
    l_list = []
    for locker,area in data[index:stop]:
        l = locker.toJSON()
        l['area_description'] = area.description
        l_list.append(l)
    return {"num_pages": num_pages,"data":l_list}
    

def get_all_lockers():
    locker_list = db.session.query(Locker,Area).join(Area).all()
    if not locker_list:
        return []
    
    data = []
    for locker,area in locker_list:
        l = locker.toJSON()
        keyH = locker.KeyH.order_by(KeyHistory.date_moved.desc()).first().id
        l['area_description'] = area.description
        current_rental = Rent.query.filter(and_(Rent.keyHistory_id == keyH, Rent.status != RStatus.VERIFIED)).first()
        if current_rental:
            l['current_rental'] = current_rental.toJSON()
        data.append(l)
    return data

def get_num_lockers():
    try:
        lockers = Locker.query.all()

        if not lockers:
            count = 1
        else:
            count = len(lockers)
       
        return count
    except:
        db.session.close()
        db.session.begin()

def get_num_locker_page(size):
    count = get_num_lockers()

    if count == 0:
        return 1

    if count%size != 0:
        return int(count/size + 1)

    return int(count/size)

def get_lockers_by_offset(size,offset):
     l_offset = (offset * size) - size
     lockers = db.session.query(Locker,Area).join(Area).limit(size).offset(l_offset)
     
     if not lockers:
        return None
     data = []
     for locker,area in lockers:
        l = locker.toJSON()
        current_rental = Rent.query.filter(and_(Rent.locker_id == l['locker_code'], Rent.status != RStatus.VERIFIED)).first()
        if current_rental:
            l['current_rental'] = current_rental.toJSON()
        l['area_description'] = area.description
        data.append(l)
     return data

def get_current_rental(id):
    current_rental = Rent.query.filter(and_(Rent.locker_id == id, Rent.status != RStatus.VERIFIED)).first()
    if current_rental:
        return current_rental.toJSON()
    return None

def get_current_locker_instance(id):
    locker = get_locker_id_locker(id)

    if not locker:
        return None
    return locker.order_by(KeyHistory.date_moved.desc()).first()


def rent_locker(id):
    locker = get_locker_id_locker(id)
    if not locker or locker.status == Status.RENTED:
        flash("locker already Rented")
        return None
    locker.status = Status.RENTED
    try:
        db.session.add(locker)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to Rent Locker. Check Error Log for more Details")
        db.session.rollback()
        return None

def not_verified(id):
    locker = get_locker_id_locker(id)
    
    if not locker :
        return None
    
    locker.status = Status.NVERIFIED
    
    try:
        db.session.add(locker)
        db.session.commit()
        
        return locker
    except SQLAlchemyError as e:
        db.session.rollback()
        create_log(id, type(e), datetime.now())
        flash("Unable to release Locker. Check Error Log for more Details")
        return None

def release_locker(id):
    locker = get_locker_id_locker(id)
    
    if not locker :
        return None
    
    locker.status = Status.FREE
    
    try:
        db.session.add(locker)
        db.session.commit()
        return locker
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to release Locker. Check Error Log for more Details")
        db.session.rollback()
        return None

def delete_locker(id):
    locker = get_locker_id_locker(id)
    if not locker:
        return None

    if locker.get_current_rent():
        flash('Can not delete a locker currently being rented')
        return None
    else:
        try:
            db.session.delete(locker)
            db.session.commit()
            return locker
        except SQLAlchemyError as e:
            create_log(id, type(e), datetime.now())
            flash("Unable to delete Locker. Check Error Log for more Details")
            db.session.rollback()
            return None
    
def update_key(id, new_key):
    locker = get_locker_id_locker(id)
    if not locker:
        return None

    if locker.get_current_rent():
        flash('Can not delete a locker currently being rented')
        return None
    else:
        try:
            new_keyHistory(new_key,locker.locker_code,datetime.now().date())
            return locker
        except SQLAlchemyError as e:
            create_log(id, type(e), datetime.now())
            flash("Unable to update key. Check Error Log for more Details")
            db.session.rollback()
            return None

def update_locker_status(id, new_status):
    locker = get_locker_id_locker(id)
    if not locker:
        return None
    
    if locker.get_current_rent():
        flash('Can not delete a locker currently being rented')
        return None
    else:
        try:
            if new_status.upper() in Status.__members__:
                locker.status = Status[new_status.upper()]
                db.session.add(locker)
                db.session.commit()
                return locker
        except SQLAlchemyError:
            db.session.rollback()
            return None

def update_locker_type(id, new_type):
    locker = get_locker_id_locker(id)
    if not locker:
        return None
        
    if locker.get_current_rent():
        flash('Can not delete a locker currently being rented')
        return None
    else:
        try:
            if new_type.upper() in LockerTypes.__members__:
                locker.locker_type = LockerTypes[new_type.upper()]
                db.session.add(locker)
                db.session.commit()
                return locker
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e.__dict__)
            create_log(id, type(e), datetime.now())
            flash("Unable to update locker status. Check Error Log for more Details")
            return None

def get_locker_rent_history(id,size,offset):
    query = db.session.query(Locker,Rent).join(Rent).filter(Locker.locker_code == id).order_by( Rent.id.desc()).all()
    if not query:
        return None

    length_rent = len(query)

    if length_rent == 0:
        num_pages = 1

    if length_rent%size != 0:
        num_pages = int((length_rent/size) + 1)
    else:
        num_pages = int(length_rent/size)

    index = (offset * size) - size
    stop = (offset * size)

    if(stop > length_rent):
        stop = length_rent
    r_list = []

    for l,r in query[index:stop]:
        r_list.append(r.toJSON())

    return {"num_pages":num_pages,"data":r_list}
    
def getStatuses():
    return [ e.value for e in Status ]

def getLockerTypes():
    return [ e.value for e in LockerTypes]

def swap_key(id1, id2):
    locker1 = get_locker_id_locker(id1)
    locker2 = get_locker_id_locker(id2)
    if locker1 is None or locker2 is None:
        return None
    temp = locker1.KeyH.order_by(KeyHistory.date_moved.desc()).first().key_id
    temp2 = locker2.KeyH.order_by(KeyHistory.date_moved.desc()).first().key_id
    try:
        new_keyHistory(temp2,locker1.locker_code,datetime.now().date())
        new_keyHistory(temp,locker2.locker_code,datetime.now().date())
        return [locker1,locker2]
    except SQLAlchemyError:
        db.session.rollback()
        return None

def get_all_locker_names():
   queryLocker = Locker.query.all()
   if not queryLocker:
    return []
   return [l.locker_code for l in queryLocker]

def get_lockers_available_names():
    locker_list = Locker.query.filter(Locker.status == Status.FREE).all()
    if not locker_list:
        return []
    return [l.locker_code for l in locker_list]