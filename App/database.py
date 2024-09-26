from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def get_migrate(app):
    return Migrate(app, db)

def create_db():
    db.create_all()
    
def init_db(app):
    db.init_app(app)




#Model for Lecturer/TA/Tutor all under one model
class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False) #this is to determine whether staff is lec, ta or tut
    

    def __repr__(self):
        return f"<Staff {self.name}, Role: {self.role}>"

#stuff to handle the many to many relationships
course_staff = db.Table('course staff',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('staff.id', db.Integer, db.ForeignKey('staff.id'),primary_key=True)
)



#Model for the courses
class Course(db.Model):
    __tablename__= 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    staff = db.relationship('Staff', secondary=course_staff, lazy='subquery',
             backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return f"<Course {self.name}>"



