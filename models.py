from app import db
from flask_user import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    fist_name = db.Column(db.String(127), nullable=False)
    last_name = db.Column(db.String(127), nullable=False)
    password = db.Column(db.String(127), nullable=False)