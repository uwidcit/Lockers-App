from datetime import datetime
from App.database import db

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rent_id = db.Column(db.Integer, db.ForeignKey("rent.id"), nullable = False)
    comment = db.Column(db.String, nullable= False) 
    date_created = db.Column(db.DateTime, nullable = False)

    def __init__(self,rent_id,comment,date_created):
        self.rent_id = rent_id
        self.comment = comment
        self.date_created = date_created
    def toJSON(self):
       return{
            'id':self.id,
            'rent_id':self.rent_id,
            'comment':self.comment,
            'date_created':datetime.strftime(self.date_created,'%Y-%m-%d')
            }