from app import db
from models import Users, Role

db.drop_all()
db.create_all()
admin_role = Role(name='admin')
db.session.add(admin_role)
db.session.commit()
user = User(username='user', first_name='first', last_name='last', role_id=admin_role.id)
user.set_password('password')
db.session.add(user)
db.session.commit()
db.session.close()