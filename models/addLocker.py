from flask_wtf import FlaskForm 
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email

class AddLocker(FlaskForm):
    locker_code = StringField('locker_code', validators=[InputRequired()])
    area = SelectField('area', choices =[('1', 'FST'),('2','ENG'), ('3','FSS')], option_widget="input",validators=[InputRequired()])
    key_id = SelectField('key_id', choices =['2'], validators=[InputRequired()])
    locker_type = SelectField('locker_type', choices =['3'], validators=[InputRequired()])
    submit = SubmitField('Add Locker', render_kw={'class': 'btn waves-effect waves-light white-text'} )
