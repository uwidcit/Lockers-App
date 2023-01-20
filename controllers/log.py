from sqlalchemy.exc import IntegrityError,NoReferenceError,NoResultFound

def create_log(exception, id):
    if exception == IntegrityError:
        return 'A record already exists with value ' +id
    if exception == NoResultFound:
        return 'Record doesnt exists'
    if exception == NoReferenceError:
        return 'Reference to value doesn''t exist'
    


