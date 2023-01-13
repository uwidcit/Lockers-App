from models import Log
from flask import flash
from datetime import datetime
from database import db 
from sqlalchemy.exc import SQLAlchemyError

def create_log(id, message,timestamp):
    try:
        log = Log(id, message,timestamp)
        db.session.add(log)
        db.session.commit(log)
        return log
    except SQLAlchemyError as e:
        create_log(id, type(e), datetime.now())
        flash("Unable to log event. Check Error Log for more Details")
        db.session.rollback()   
        return None

def get_all_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).all()

    if not logs:
        return None

    return[l.toJSON() for l in logs]