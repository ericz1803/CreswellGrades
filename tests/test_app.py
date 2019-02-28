import os
import sys
sys.path.append("..")
os.environ['APP_SETTINGS'] = 'config.TestingConfig'
os.environ['DATABASE_URL'] = 'postgresql://localhost/gradestest'

import warnings
import unittest
from app import app, db
from models import Users, Role
from flask import request, jsonify

class TestUsernameExistsJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """empty database"""
        db.session.commit()
        db.session.close()
        db.drop_all()
        db.create_all()
    
    def setUp(self):
        self.admin_role = Role(name='admin')
        db.session.add(self.admin_role)
        self.user = Users(username='user', first_name='first', last_name='last', role_id=self.admin_role.id)
        self.user.set_password('password')
        db.session.add(self.user)

    def tearDown(self):
        db.session.rollback()

    def testUsernameTakenTrue(self):
        with app.test_client() as c:
            resp = c.get('/ajax/username-taken/user')
            json_data = resp.get_json()
            self.assertTrue(json_data["taken"]) 
    
    def testUsernameTakenFalse(self):
        with app.test_client() as c:
            resp = c.get('/ajax/username-taken/notuser')
            json_data = resp.get_json()
            self.assertFalse(json_data["taken"]) 

if __name__ == '__main__':
    warnings.warn("Only running app tests.")
    print("To run all tests run 'python test.py'")
    unittest.main()