from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email

class Add(FlaskForm):
    locker_code = StringField('locker_code', validators=[InputRequired()])
    area = SelectField(u'area', choices=[('SAC', 'SAC'), ('ENG', 'Engineer'), ('FST', 'FST'), ('FSS', 'FSS')])
    locker_type  = SelectField(u'locker_type', choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Combination', 'Combination')])
    status  = SelectField(u'Programming Language', choices=[('Rented', 'Rented'), ('Repair', 'Repair'), ('Free', 'Free')])
    key_id = StringField('key_id', validators=[InputRequired()])
    submit = SubmitField('Sign Up', render_kw={'class': 'btn waves-effect waves-light white-text'})
    
    