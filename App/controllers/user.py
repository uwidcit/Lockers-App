from App.models import User,Assistant
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def create_assistant(username,password):
    newuser = Assistant(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def change_password(id,current_pass,new_pass):
    user = get_user(id)

    if not user:
        return None

    if user.check_password(current_pass):
        try:
            user.set_password(new_pass)
            db.session.add(user)
            db.session.commit()
            return user
        except:
            db.session.rollback()
            return None
    else:
         raise Exception('Current password is incorrect')

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_assistant(id):
    return Assistant.query.get(id)

def set_assistant_password(id,password):
    assistant = get_assistant(id)

    if not assistant:
        return None
    try:
        assistant.set_password(password)
        db.session.add(assistant)
        return db.session.commit()
    except:
        db.session.rollback()
        return None

def delete_assistant(id):
    assistant = get_assistant(id)

    if not assistant:
        return None
    try:
    
        db.session.delete(assistant)
        return db.session.commit()
    except:
        db.session.rollback()
        return None

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def get_all_assistant():
    users = Assistant.query.all()
    if not users:
        return None
    return users

def get_all_assistant_by_offset(size,offset):
    users = Assistant.query.all()
    if not users:
        return {"num_pages":1,"data":[]}
    
    length_assistant = len(users)
    if length_assistant == 0:
         num_pages = 1
    
    if length_assistant%size != 0:
        num_pages = int((length_assistant/size) + 1)
    else:
        num_pages = int(length_assistant/size)
    
    index = (offset * size) - size
    stop = (offset * size)

    if(stop > length_assistant):
        stop = length_assistant
    
    s_list = []

    for d in users[index:stop]:
        s_list.append(d.toJSON())

    return {"num_pages":num_pages,"data":s_list}

def get_all_assistant_json():
    users = Assistant.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def get_current_user(id):
    user = get_user(id)
    if user:
        return user.username
    return None  