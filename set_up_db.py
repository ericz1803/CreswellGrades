from app import db
from models import Users, Role

db.drop_all()
db.create_all()
admin_role = Role(name='admin')
db.session.add(admin_role)
student_role = Role(name='student')
db.session.add(student_role)
teacher_role = Role(name='teacher')
db.session.add(teacher_role)
db.session.commit()
db.session.close()