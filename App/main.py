import os,sys
from os import path
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from flaskwebgui import FlaskUI
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta

from App.database import create_db, get_migrate
from App.config import config

from App.controllers import (
    setup_flask_login
)

from App.views import (
    user_views,
    transactionLog_views,
    rentType_views,
    rent_views,
    student_views,
    locker_views,
    area_views,
    index_views,
    masterkey_views,
    key_views,
    report_views,
)

# New views must be imported and added to this list
views = [
    user_views,
    transactionLog_views,
    rentType_views,
    rent_views,
    student_views,
    locker_views,
    area_views,
    index_views,
    masterkey_views,
    key_views,
    report_views,
]

def add_views(app, views):
    for view in views:
        app.register_blueprint(view)

def configure_app(app, config, overrides):
    for key, value in config.items():
        if key in overrides:
            app.config[key] = overrides[key]
        else:
            app.config[key] = config[key]

def create_app(config_overrides={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    configure_app(app, config, config_overrides)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    create_db(app)
    setup_flask_login(app)
    app.app_context().push()
    return app
