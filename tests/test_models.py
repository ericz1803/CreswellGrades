import os
import sys
sys.path.append("..")
os.environ['APP_SETTINGS'] = 'config.TestingConfig'
os.environ['DATABASE_URL'] = 'postgresql://localhost/gradestest'

import warnings
import unittest
from app import app, db
from models import Users, Role, Class, GradeFactor, Assignment, AssignmentResult

class TestUsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.session.commit()
        db.session.close()
        db.drop_all()
        db.create_all()
    
    def setUp(self):
        self.admin_role = Role(name='admin')
        db.session.add(self.admin_role)

    def tearDown(self):
        db.session.rollback()

    def test_normal_insert(self):
        user = Users(username='user', first_name='first', last_name='last', role_id=self.admin_role.id)
        user.set_password('password')
        db.session.add(user)
        self.assertEqual(len(Users.query.all()), 1)

    def test_set_password(self):
        user = Users(username='user', first_name='first', last_name='last', role_id=self.admin_role.id)
        user.set_password('password')
        db.session.add(user)
        pw = Users.query.filter_by(username='user').first().password_hash
        self.assertNotEqual(pw, 'password')

    def test_check_correct_password_returns_true(self):
        user = Users(username='user', first_name='first', last_name='last', role_id=self.admin_role.id)
        user.set_password('password')
        db.session.add(user)
        self.assertTrue( Users.query.filter_by(username='user').first().check_password('password'))

    def test_check_incorrect_password_returns_false(self):
        user = Users(username='user', first_name='first', last_name='last', role_id=self.admin_role.id)
        user.set_password('password')
        db.session.add(user)
        self.assertFalse( Users.query.filter_by(username='user').first().check_password('1234'))

class TestClass(unittest.TestCase):
    def test_normal_class(self):
        pass


if __name__ == '__main__':
    warnings.warn("Only running model tests.")
    print("To run all tests run 'python test.py'")
    unittest.main()