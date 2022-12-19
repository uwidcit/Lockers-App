from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField,DecimalField,HiddenField, DateField
from wtforms.validators import InputRequired, EqualTo, Email

from controllers import (
    getLockerTypes,
    getStatuses,
    getKey,
    getT_Type
)

class LockerAdd(FlaskForm):
    status = getStatuses()
    status.remove('Rented')
    locker_code = StringField('locker_code', validators=[InputRequired()])
    locker_type  = SelectField(u'locker_type', choices= getLockerTypes())
    status  = SelectField(u'status', choices=status)
    key = SelectField('key', choices= getKey(), validators=[InputRequired()])
    submit = SubmitField('Add Locker', render_kw={'class': 'btn waves-effect waves-light white-text'})

class AreaAdd(FlaskForm):
    l_code = StringField('l_code', render_kw={'disabled':''})
    locker_code = HiddenField('locker_code')
    description  = StringField('description', validators=[InputRequired()])
    longitude = DecimalField('longitude', validators=[InputRequired()])
    latitude = DecimalField('latitude', validators=[InputRequired()])
    submit = SubmitField('Add Area', render_kw={'class': 'btn waves-effect waves-light white-text'})

class TransactionAdd(FlaskForm):
    rent_id = StringField('rent_id', validators=[InputRequired()])
    currency = StringField('currency',validators=[InputRequired()])
    transaction_date = DateField('transaction_date',validators=[InputRequired()])
    amount = DecimalField('amount',validators=[InputRequired()],places=2)
    description = StringField('description',validators=[InputRequired()])
    t_type = SelectField('t_type',choices=getT_Type())
    submit = SubmitField('Submit Payment', render_kw={'class': 'btn waves-effect waves-light white-text'})

class RentTypeAdd(FlaskForm):
    period = StringField('period', validators=[InputRequired()])
    type =  SelectField(u'locker_type', choices= getLockerTypes())
    price = DecimalField('price',validators=[InputRequired()],places=2)
    submit = SubmitField('New Price Model', render_kw={'class': 'btn waves-effect waves-light white-text'})



    
    
    