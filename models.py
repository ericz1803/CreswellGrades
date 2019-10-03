from app import app, db
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin, UserManager
import flask_bcrypt
import datetime

db.metadata.clear()
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    user = db.relationship('Users', backref='role', lazy=True)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(127), nullable=False)
    last_name = db.Column(db.String(127), nullable=False)
    password_hash = db.Column(db.LargeBinary(60), nullable=False)
    password_reset = db.Column(db.String(63))
    email = db.Column(db.String(63))
    
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    class_student_link = db.relationship('ClassStudentLink', backref='student', passive_deletes=True)
    assignmentresult = db.relationship('AssignmentResult', backref='student', passive_deletes=True)

    def set_password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password)
    
    def check_password(self, check):
        return flask_bcrypt.check_password_hash(self.password_hash, check)

class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    teacher = db.relationship('Users', backref='classes')

    name = db.Column(db.String(127), nullable=False, unique=True)
    join_code = db.Column(db.String(127), nullable=False, unique=True)

    grade_factor = db.relationship('GradeFactor', backref='class_', passive_deletes=True)
    grade_scale = db.relationship('GradeScale', backref='class_', passive_deletes=True)
    assignment = db.relationship('Assignment', backref='class_', passive_deletes=True)
    class_student_link = db.relationship('ClassStudentLink', backref='class_', passive_deletes=True)

class GradeFactor(db.Model):
    __tablename__ = 'gradefactor'
    id = db.Column(db.Integer, primary_key=True)
    
    category1_name = db.Column(db.String(63), nullable=False)
    category1_weight = db.Column(db.Float())
    category1_drop = db.Column(db.Integer(), default=0)
    category2_name = db.Column(db.String(63))
    category2_weight = db.Column(db.Float())
    category2_drop = db.Column(db.Integer(), default=0)
    category3_name = db.Column(db.String(63))
    category3_weight = db.Column(db.Float())
    category3_drop = db.Column(db.Integer(), default=0)
    category4_name = db.Column(db.String(63))
    category4_weight = db.Column(db.Float())
    category4_drop = db.Column(db.Integer(), default=0)
    category5_name = db.Column(db.String(63))
    category5_weight = db.Column(db.Float())
    category5_drop = db.Column(db.Integer(), default=0)
    category6_name = db.Column(db.String(63))
    category6_weight = db.Column(db.Float())
    category6_drop = db.Column(db.Integer(), default=0)
    category7_name = db.Column(db.String(63))
    category7_weight = db.Column(db.Float())
    category7_drop = db.Column(db.Integer(), default=0)
    category8_name = db.Column(db.String(63))
    category8_weight = db.Column(db.Float())
    category8_drop = db.Column(db.Integer(), default=0)
    #points based option
    points_based = db.Column(db.Boolean, default=False)

    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete='CASCADE'))

class GradeScale(db.Model):
    __tablename__ = 'gradescale'
    id = db.Column(db.Integer, primary_key=True)

    a_b = db.Column(db.Float(), nullable=False)
    b_c = db.Column(db.Float(), nullable=False)
    c_d = db.Column(db.Float(), nullable=False)
    d_f = db.Column(db.Float(), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete='CASCADE'))

class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True)
    assignment_name = db.Column(db.String(127), nullable=False)
    assignment_type = db.Column(db.Integer, nullable=False)
    assignment_date = db.Column(db.Date(), default=datetime.date.today())
    total_points = db.Column(db.Float(), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete='CASCADE'))
    assignment_result = db.relationship('AssignmentResult', backref='assignment', passive_deletes=True)

class AssignmentResult(db.Model):
    __tablename__ = 'assignmentresult'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id', ondelete='CASCADE'))
    points_earned = db.Column(db.Float(), nullable=False)
    
class ClassStudentLink(db.Model):
    __tablename__ = 'classstdentlink'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete='CASCADE'))