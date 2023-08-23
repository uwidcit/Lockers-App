from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def admin_only(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if(not current_user.isAdmin()):
            return redirect(url_for("index_views.unauthorized_page"))
        return f(*args, **kwargs)
    return decorated_function
