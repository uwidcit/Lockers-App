from App.models import RentTypes,Rent
from App.models.rentTypes import Types
from App.database import db
from sqlalchemy import and_,or_
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def new_rentType(period_from, period_to, type, price):
    try:
        rentType = RentTypes(period_from,period_to,type,price)
        db.session.add(rentType)
        db.session.commit()
        return rentType
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

def get_rentType_by_id(id):
    rentType = RentTypes.query.filter_by(id = id).first()

    if not rentType:
        return None

    return rentType

def get_rentType_daily_period(period_from, period_to):
    rentType = RentTypes.query.filter(and_(RentTypes.period_to >= period_to, RentTypes.period_from <= period_from,RentTypes.type == Types.DAILY)).first()
     
    if not rentType:
        return None

    return rentType

def get_rentType_period(period_to):
    rentType = RentTypes.query.filter_by(period_to = period_to)

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]

def get_rentType_price(price):
    rentType = RentTypes.query.filter_by(price = price)

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]

def update_rentType_price(id,new_price):
    #first check to see if a rentType exist in rent
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        return []
    try:
        rentType = get_rentType_by_id(id)

        if not rentType:
            return None
        rentType.price = new_price
        db.session.add(rentType)
        db.session.commit()
        return rentType
    except SQLAlchemyError as e:
        db.session.rollback()
        return None

def update_rentType_period(id, period_from, period_to):
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        return []

    rent_type = get_rentType_by_id(id)

    if not rent_type:
        return None
    
    rent_type.period_from = period_from
    rent_type.period_to = period_to
    try:
        db.session.add(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError as e:
        db.session.rollback()
        return None

def update_rentType_type(id,type):
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        return []

    rent_type = get_rentType_by_id(id)

    if not rent_type:
        return []
    
    try:
        if type.upper() in Types.__members__:
            rent_type.type = Types[type.upper()]
            db.session.add(rent_type)
            db.session.commit()
            return rent_type
    except SQLAlchemyError:
        db.session.rollback()
        return []
        
def delete_rent_type(id):
    rent = Rent.query.filter_by(rent_type = id).first()
    
    if rent:
        return None

    rent_type = get_rentType_by_id(id)

    if not rent_type:
        return None
    try:
        db.session.delete(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError:
        db.session.rollback()
        return []    

def get_All_rentType():
    rentType = RentTypes.query.filter(RentTypes.type != Types.KEYREPLACEMENT).all()

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]

def get_All_rentType_group():
    rentType = RentTypes.query.filter(RentTypes.type != Types.KEYREPLACEMENT).all()

    if not rentType:
        return None

    fixed = []
    rates = []

    for r in rentType:
        if r.type == Types.DAILY or r.type == Types.HOURLY:
            fixed.append(r.toJSON())
        else:
            rates.append(r.toJSON())
    data = {
        'fixed':fixed,
        'rates': rates
    }
    return data

def get_addtional_rentTypes():
    rentType = RentTypes.query.filter(RentTypes.type == Types.KEYREPLACEMENT).all()

    if not rentType:
        return None

    return [rt.toJSON() for rt in rentType]

def get_all_rentType_tuple():
    rentType = get_All_rentType()
    rentTuple = []
    if not rentType:
        return None
    
    for r in rentType:
        r['period_from'] = datetime.strptime(r['period_from'], '%Y-%m-%d')
        r['period_to'] = datetime.strptime(r['period_to'], '%Y-%m-%d')
        rentTuple =  rentTuple + [(r["id"], r["type"]+" $"+str(r["price"]) +" Period: "+ str(r["period_from"].year) +'/'+str(r["period_from"].month) + " to " + str(r["period_to"].year) +'/'+ str(r["period_to"].month))]

    return rentTuple

def get_all_rentType_current():
    rentType = RentTypes.query.filter(RentTypes.period_to >= datetime.today().date()).all()
    rentTuple = []
    if not rentType:
        return None
    
    for r in rentType:
        rentTuple =  rentTuple + [(r.id, r.type.value+" $"+str(r.price) +" Period: "+ str(r.period_from.year) +'/'+str(r.period_from.month) + " to " + str(r.period_to.year) +'/'+ str(r.period_to.month))]

    return rentTuple


def get_rt_Type():
    data = {
        "Semester":[],
        "Rate":[],
        "Yearly":[]
    }
    for rt in Types:
        if rt.value.__contains__("Semester"):
            data["Semester"].append((rt.name, rt.value))
        elif rt.value.__contains__("Yearly"):
            data["Yearly"].append((rt.name, rt.value))
        else:
           data["Rate"].append((rt.name, rt.value))
    return data

def get_rentType_by_offset(size,offset):
    l_offset = (offset * size) - size

    count = get_All_rentType()

    if not count:
        count = 1
    else:
        count = len(count)
    if count == 0:
        count = 1

    if count%size != 0:
        count = int(count/size + 1)

    rentTypes = RentTypes.query.limit(size).offset(l_offset)

    if not rentTypes:
        return None
    
    r_list = []

    for r in rentTypes:
        r_list.append(r.toJSON())
    
    return {"num_pages":count, "data":r_list}

def search_rentType(query,size,offset):
    try:
        int_query = int(query)
        data = RentTypes.query.filter(RentTypes.id == int_query, RentTypes.price == query).all()
    except:
        raise Exception('Invalid search data entered')

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

    rt_list = []

    for price in data[index:stop]:
        rt_list.append(price.toJSON())
    return {"num_pages":num_pages,"data":rt_list}



    

