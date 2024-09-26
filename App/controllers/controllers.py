from App.controllers import *
from App.database import db, Course, Staff

#Controllers to create a course
def create_course(course_name):
    course=Course(name=course_name)
    db.session.add(course)
    db.session.commit()
    return course

#Controller to create staff i.e lecturer/ta/tutor
def create_staff(staff_name, staff_role):
    staff = Staff(name=staff_name, role=staff_role)
    db.session.add(staff)
    db.session.commit()
    return staff

#Controller to assign staff to a course
def assign_staff_to_course(course_id, staff_id):
    course = Course.query.get(course_id)
    staff = Staff.query.get(staff_id)
    if course and staff:
        course.staff.append(staff)
        db.session.commit()
        return True
    return False
#Controller to view staff for a course
def view_course_staff(course_id):
    course=Course.query.get(course_id)
    if course:
        return course.staff
    return []