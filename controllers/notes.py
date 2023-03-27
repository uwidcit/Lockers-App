from models import Notes
from database import db
from sqlalchemy.exc import SQLAlchemyError

def create_comment(rent_id,comment,date_created):
    try:
        new_note = Notes(rent_id,comment,date_created)
        db.session.add(new_note)
        db.session.commit()
        return new_note
    except SQLAlchemyError:
        db.session.rollback()
        return None

def get_comment(id):
    note = Notes.query.filter_by(rent_id = id).first()

    if not note:
        return None
    
    return note

def get_all_comments(id):
    notes = Notes.query.filter_by(rent_id=id).order_by(Notes.id.desc()).all()

    if not notes:
        return None
    return notes

def get_comments_offset(id,size, offset):
    notes = get_all_comments(id)

    if not notes:
        return {'num_pages':1,"data":[]}
    
    count = len(notes)

    n_list = []

    if count%size != 0:
        num_pages = int(count/size + 1)
    else:
        num_pages = int(count/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop > count):
        stop = count

    for n in notes[index:stop]:
        n_list.append(n.toJSON())

    return {'num_pages':num_pages, "data":n_list}


