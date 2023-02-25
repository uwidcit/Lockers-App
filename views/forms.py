from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField,DecimalField, DateField,DateTimeLocalField,IntegerField
from wtforms.validators import InputRequired, EqualTo, Email

from controllers import (
    getT_Type,
    get_rt_Type,
    getLockerTypes,
    getStatuses,
)

class LockerAdd(FlaskForm):
    status = getStatuses()
    status.remove('Rented')
    locker_code = StringField('locker_code', validators=[InputRequired()])
    locker_type  = SelectField(u'locker_type', choices= getLockerTypes())
    status  = SelectField(u'status', choices=status)
    key = StringField('key', validators=[InputRequired()])
    area = SelectField('area', choices=[])
    submit = SubmitField('Add Locker', render_kw={'class': 'btn waves-effect waves-light white-text'})

class AreaAdd(FlaskForm):
    description  = StringField('description', validators=[InputRequired()])
    longitude = DecimalField('longitude', validators=[InputRequired()])
    latitude = DecimalField('latitude', validators=[InputRequired()])
    submit = SubmitField('Add Area', render_kw={'class': 'btn waves-effect waves-light white-text'})

class TransactionAdd(FlaskForm):
    rent_id = StringField('rent_id', validators=[InputRequired()])
    currency = StringField('currency',validators=[InputRequired()])
    transaction_date = DateTimeLocalField('transaction_date',validators=[InputRequired()])
    amount = DecimalField('amount',validators=[InputRequired()],places=2)
    description = StringField('description',validators=[InputRequired()])
    t_type = SelectField('t_type',choices=getT_Type())
    receipt_number = IntegerField('receipt_number',validators=[InputRequired()])
    submit = SubmitField('Submit Payment', render_kw={'class': 'btn waves-effect waves-light white-text'})

class RentTypeAdd(FlaskForm):
    period_from = DateField('period_from', validators=[InputRequired()])
    period_to = DateField('period_to', validators=[InputRequired()])
    type =  SelectField('type', choices=get_rt_Type(),validators=[InputRequired()])
    price = DecimalField('price',validators=[InputRequired()],places=2)
    submit = SubmitField('New Price Model', render_kw={'class': 'btn waves-effect waves-light white-text'})

class RentAdd(FlaskForm):
    student_id = StringField('student_id', validators=[InputRequired()])
    rent_type =  SelectField('rent_type', choices=[])
    rent_date_from = DateTimeLocalField('rent_date_from', format='%Y-%m-%d %H:%M:%S')
    rent_date_to = DateTimeLocalField('rent_date_to', format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Rent', render_kw={'class': 'btn waves-effect waves-light white-text'})

class StudentAdd(FlaskForm):
    student_id = StringField('student_id', validators=[InputRequired()])
    f_name =  StringField('f_name', validators=[InputRequired()])
    l_name =  StringField('l_name', validators=[InputRequired()])
    faculty =  StringField('faculty', validators=[InputRequired()])
    p_no =  StringField('p_no', validators=[InputRequired()])
    email =  StringField('email', validators=[InputRequired(),Email()])
    submit = SubmitField('Add', render_kw={'class': 'btn waves-effect waves-light white-text'})  

class ConfirmDelete(FlaskForm):
    submit = SubmitField('Confirm Delete', render_kw={'class': 'btn waves-effect waves-light white-text'}) 

class SearchForm(FlaskForm):
    search_query = StringField('search_string', validators=[InputRequired()])
    submit = SubmitField('Search', render_kw={'class': 'btn waves-effect waves-light white-text'}) 
    
class masterKeyForm(FlaskForm):
    masterkey_id = StringField('masterkey_id', validators=[InputRequired()])
    series = StringField('series', validators=[InputRequired()])
    date_added = DateField('date_added', validators=[InputRequired()])
    key_type = SelectField('key_type', choices=["Combination", "Lock"])
    submit = SubmitField('Add Master Key', render_kw={'class': 'btn waves-effect waves-light white-text'})