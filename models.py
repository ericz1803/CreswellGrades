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
    

    assignmentresult = db.relationship('AssignmentResult', back_populates="student")

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

class GradeFactor(db.Model):
    __tablename__ = 'gradefactor'
    id = db.Column(db.Integer, primary_key=True)
    
    category1_name = db.Column(db.String(63), nullable=False)
    category1_weight = db.Column(db.Float(), nullable=False)
    category2_name = db.Column(db.String(63))
    category2_weight = db.Column(db.Float())
    category3_name = db.Column(db.String(63))
    category3_weight = db.Column(db.Float())
    category4_name = db.Column(db.String(63))
    category4_weight = db.Column(db.Float())
    category5_name = db.Column(db.String(63))
    category5_weight = db.Column(db.Float())
    category6_name = db.Column(db.String(63))
    category6_weight = db.Column(db.Float())
    category7_name = db.Column(db.String(63))
    category7_weight = db.Column(db.Float())
    category8_name = db.Column(db.String(63))
    category8_weight = db.Column(db.Float())

    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    class_ = db.relationship('Class', uselist=False)

class GradeScale(db.Model):
    __tablename__ = 'gradescale'
    id = db.Column(db.Integer, primary_key=True)

    a_b = db.Column(db.Float(), nullable=False)
    b_c = db.Column(db.Float(), nullable=False)
    c_d = db.Column(db.Float(), nullable=False)
    d_f = db.Column(db.Float(), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    class_ = db.relationship('Class', uselist=False)

class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True)
    assignment_name = db.Column(db.String(127), nullable=False)
    assignment_type = db.Column(db.Integer, nullable=False)
    assignment_date = db.Column(db.Date(), default=datetime.date.today())
    total_points = db.Column(db.Float(), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    Class = db.relationship('Class')
    assignment_result = db.relationship('AssignmentResult', back_populates='assignment')

class AssignmentResult(db.Model):
    __tablename__ = 'assignmentresult'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    student = db.relationship('Users', back_populates='assignmentresult')
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    assignment = db.relationship('Assignment', back_populates='assignment_result')
    points_earned = db.Column(db.Float(), nullable=False)
    
class ClassStudentLink(db.Model):
    __tablename__ = 'classstdentlink'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    student = db.relationship('Users')
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    class_ = db.relationship('Class')