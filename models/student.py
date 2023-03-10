from database import db
from enum import Enum
class RentStanding(Enum):
    GOOD = "GOOD"
    RENTING = "RENTING"
    OVERDUE = "OVERDUE"
    OWED = "OWED"

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String, nullable= False)	
    last_name = db.Column(db.String, nullable= False)	
    faculty = db.Column(db.String(3), nullable= False)	
    phone_number = db.Column(db.String, nullable= False) 	
    email = db.Column(db.String, nullable= False, unique = True)
    rentStanding = db.Column(db.Enum(RentStanding), nullable=False)
    

    def __init__(self, student_id, first_name, last_name,faculty, phone_number, email):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.faculty = faculty
        self.phone_number = phone_number
        self.email = email
        self.rentStanding = RentStanding.GOOD
        
    def toJSON(self):
        return{
            'student_id':self.student_id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'faculty':self.faculty,
            'phone_number':self.phone_number,
            'email':self.email,
            'rentStanding':self.rentStanding.value
        }