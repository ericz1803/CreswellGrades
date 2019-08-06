from app import db
from models import Users, AssignmentResult, Assignment


user = Users.query.filter_by(id=3).first_or_404()
assignment = Assignment.query.filter_by(id=3).first_or_404()
new_assignment_result = AssignmentResult(student_id=user.id, assignment_id=assignment.id, points_earned=3)

db.session.add(new_assignment_result)
db.session.commit()
db.session.close()