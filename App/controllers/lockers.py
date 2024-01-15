from App.models import Locker
from App.models import Area, Rent, KeyHistory,Active
from App.models.rent import RentStatus as RStatus
from App.models.locker import LockerStatus as Status, LockerTypes
from App.database import db
from App.controllers.log import create_log
from App.controllers.area import get_area_by_id,get_area_by_description
from App.controllers.key_history import new_keyHistory,getKeyHistory,deactivate
from datetime import datetime
from sqlalchemy import or_,and_
from sqlalchemy.exc import SQLAlchemyError

def add_new_locker(locker_code,locker_type,status,key_id,area):
    try:
        if len(key_id) == 0 or not key_id:
            key_id = 'NoKey'
            status = 'Repair'
        locker = Locker(locker_code,locker_type,status,area)
        db.session.add(locker)
        db.session.commit()
        new_keyHistory(key_id,locker.locker_code,datetime.now().date())
        return locker
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

def restore_locker(locker_id,locker_type,status,area):
    try:
        locker = Locker(locker_id,locker_type,status,area)
        db.session.add(locker)
        db.session.commit()
        return locker
    except SQLAlchemyError as e:
        db.session.rollback()
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
    locker = db.session.query(Locker,Area,KeyHistory).join(Area,KeyHistory).filter(Locker.locker_code == id,KeyHistory.isActive == Active.ACTIVE).first()
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
    locker_list = db.session.query(Locker,Area,KeyHistory).join(Area,KeyHistory).filter(KeyHistory.isActive == Active.ACTIVE).all()

    if not locker_list:
        return []
    
    data = []

    for locker,area,keyHistory in locker_list:
        l = locker.toJSON()
        l['area_description'] = area.description
        l['key'] = keyHistory.key_id

        #if l['status'] !='Repair' and (l['status'] == 'Rented' or l['status'] == 'Not Verified') :
           #if l['key_history']['rent']:
               # from App.controllers import update_rent
                #for r in l['key_history']['rent']:
                   # if r["status"] != "Verified":
                       #l['current_rental'] = update_rent(r['id']).toJSON()
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
        keyH = locker.KeyH.order_by(KeyHistory.id.desc()).first().id
        current_rental =  Rent.query.filter(and_(Rent.keyHistory_id == keyH, Rent.status != RStatus.VERIFIED)).first()
        if current_rental:
            l['current_rental'] = current_rental.toJSON()
        l['area_description'] = area.description
        data.append(l)
     return data

def get_current_rental(id):
    locker = get_locker_id_locker(id)
    if locker is None:
        return None
    keyH = locker.KeyH.order_by(KeyHistory.id.desc()).first().id
    current_rental =  Rent.query.filter(and_(Rent.keyHistory_id == keyH, Rent.status != RStatus.VERIFIED)).first()
    if current_rental:
        return current_rental.toJSON()
    return None
def get_current_rental_c(id):
    locker = get_locker_id_locker(id)
    if locker is None:
        return None
    keyH = locker.KeyH.order_by(KeyHistory.id.desc()).first().id
    current_rental =  Rent.query.filter(and_(Rent.keyHistory_id == keyH, Rent.status != RStatus.VERIFIED)).first()
    if current_rental:
        return current_rental
    return None

def get_current_locker_instance(id):
    locker = get_locker_id_locker(id)

    if not locker:
        return None
    return locker.KeyH.order_by(KeyHistory.id.desc()).first()


def rent_locker(id):
    locker = get_locker_id_locker(id)
    if not locker or locker.status == Status.RENTED:
        return None
    locker.status = Status.RENTED
    try:
        db.session.add(locker)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        db.session.rollback()
        return None

def not_verified(id):
    keyH = getKeyHistory(id)
    locker = get_locker_id_locker(keyH.locker_id)
    
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
        return None

def release_locker(id):
    keyH = getKeyHistory(id)
    locker = get_locker_id_locker(keyH.locker_id)
    if not locker:
        return None
    
    locker.status = Status.FREE
    
    try:
        db.session.add(locker)
        db.session.commit()
        return locker
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

def delete_locker(id):
    locker = get_locker_id_locker(id)
    if not locker:
        return None

    if get_current_rental(id):
        return None
    else:
        try:
            db.session.delete(locker)
            db.session.commit()
            return locker
        except SQLAlchemyError as e:
            db.session.rollback()
            return None
    
def update_key(id, new_key):
    if len(new_key) == 0 or new_key is None:
        raise Exception('Key cannot be empty')
    locker = get_locker_id_locker(id)
    if not locker:
        return None

    if get_current_rental(id):
        return None
    else:
        keyH1 = locker.KeyH.order_by(KeyHistory.id.desc()).first()
        keyH2 = KeyHistory.query.filter(KeyHistory.key_id == new_key).order_by(KeyHistory.id.desc()).first()
        if keyH2:
            swap_key(keyH1.locker_id,keyH2.locker_id)
        else:
            new_keyHistory(new_key,id,datetime.now())
        return locker

def update_locker_status(id, new_status):
    if len(new_status) == 0 or new_status is None:
        raise Exception('Locker Status cannot be set to empty')
    locker = get_locker_id_locker(id)
    if not locker:
        return None
    
    if get_current_rental(id):
        return None
    else:
        if locker.status.value == new_status:
            return locker
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
    if len(new_type) == 0 or new_type is None:
        raise Exception('Locker Type cannot be empty')
    locker = get_locker_id_locker(id)
    if not locker:
        return None
        
    if get_current_rental(id):
        return None
    else:
        if locker.locker_type.value == new_type:
            return locker
        try:
            if new_type.upper() in LockerTypes.__members__:
                locker.locker_type = LockerTypes[new_type.upper()]
                db.session.add(locker)
                db.session.commit()
                return locker
        except SQLAlchemyError as e:
            db.session.rollback()
            create_log(id, type(e), datetime.now())
            return None

def get_locker_rent_history(id,size,offset):
    query = db.session.query(KeyHistory,Rent).join(Rent).filter(KeyHistory.locker_id == id).order_by(Rent.id.desc()).all()
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
    temp = locker1.KeyH.order_by(KeyHistory.id.desc()).first()
    temp2 = locker2.KeyH.order_by(KeyHistory.id.desc()).first()
    try:
        deactivate(temp.id)
        deactivate(temp2.id)
        new_keyHistory(temp2.key_id,locker1.locker_code,datetime.now().date())
        new_keyHistory(temp.key_id,locker2.locker_code,datetime.now().date())
        locker2 = get_locker_id(id2)
        locker1 = get_locker_id(id1)
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