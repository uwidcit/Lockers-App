from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField,DecimalField,HiddenField
from wtforms.validators import InputRequired, EqualTo, Email

from controllers import (
    getLockerTypes,
    getStatuses,
    getKey
)

class LockerAdd(FlaskForm):
    locker_code = StringField('locker_code', validators=[InputRequired()])
    locker_type  = SelectField(u'locker_type', choices= getLockerTypes())
    status  = SelectField(u'Programming Language', choices=getStatuses())
    key = SelectField('key', choices= getKey(), validators=[InputRequired()])
    submit = SubmitField('Add Locker', render_kw={'class': 'btn waves-effect waves-light white-text'})

class AreaAdd(FlaskForm):
    l_code = StringField('l_code', render_kw={'disabled':''})
    locker_code = HiddenField('locker_code')
    description  = StringField('description', validators=[InputRequired()])
    longitude = DecimalField('longitude', validators=[InputRequired()])
    latitude = DecimalField('latitude', validators=[InputRequired()])
    submit = SubmitField('Add Area', render_kw={'class': 'btn waves-effect waves-light white-text'})
    
    