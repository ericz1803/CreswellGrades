import os
import sys
sys.path.append("..")
os.environ['APP_SETTINGS'] = 'config.TestingConfig'
os.environ['DATABASE_URL'] = 'postgresql://localhost/gradestest'

import warnings
import unittest
from app import app, db
from models import Users, Role
from flask import request, jsonify, url_for, session

class TestUsernameExistsJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #empty database
        db.session.commit()
        db.session.close()
        db.drop_all()
        db.create_all()

        #set up data
        admin_role = Role(name='admin')
        db.session.add(admin_role)
        user = Users(username='user', first_name='first', last_name='last', role_id=admin_role.id)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        db.session.close()

    @classmethod
    def tearDownClass(cls):
        #empty database again
        db.drop_all()
        db.session.commit()
        db.session.close()

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

class TestHome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #empty database
        db.session.commit()
        db.session.close()
        db.drop_all()
        db.create_all()

        #set up database
        admin_role = Role(name='admin')
        db.session.add(admin_role)
        user_role = Role(name='user')
        db.session.add(user_role)
        teacher_role = Role(name='teacher')
        db.session.add(teacher_role)
        user = Users(username='user', first_name='first', last_name='last', role_id=user_role.id)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        db.session.close()

    @classmethod
    def tearDownClass(cls):
        #empty database again
        db.drop_all()
        db.session.commit()
        db.session.close()

    def testNoUserId(self):
        with app.test_client() as c:
            resp = c.get('/user/1')
            self.assertEqual(resp.status_code, 302)
            self.assertIn('http://localhost/login?next', resp.headers['location'])
    
    def testWrongUserId(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['user_id'] = 1
            resp = c.get('/user/2')
            self.assertEqual(resp.status_code, 403)
    
    def testCorrectUserId(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                session['user_id'] = 1
            resp = c.get('/user/1')
            self.assertEqual(resp.status_code, 200)


class TestAdminInterfacePrivileges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #empty database
        db.session.commit()
        db.session.close()
        db.drop_all()
        db.create_all()

        #set up data
        admin_role = Role(name='admin')
        db.session.add(admin_role)
        user_role = Role(name='user')
        db.session.add(user_role)
        admin = Users(username='admin', first_name='first', last_name='last', role=admin_role)
        admin.set_password('password')
        db.session.add(admin)
        user = Users(username='user', first_name='first', last_name='last', role=user_role)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        db.session.close()
 
    @classmethod
    def tearDownClass(cls):
        #empty database again
        db.drop_all()
        db.session.commit()
        db.session.close()

    def testIsAdmin(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                #admin
                session['user_id'] = 1
            resp = c.get('/admin')
            self.assertIn('http://localhost/admin/', resp.headers['location'])
            self.assertEqual(resp.status_code, 301)

    def testIsNotAdminHomepage(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                #normal user
                session['user_id'] = 2
            resp = c.get('/admin')
            self.assertTrue(resp.status_code, 403)

    def testIsNotAdminSubpage(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                #normal user
                session['user_id'] = 2
            resp = c.get('/admin/users')
            self.assertTrue(resp.status_code, 403)

    def testIsNotAdminSubpage2(self):
        with app.test_client() as c:
            with c.session_transaction() as session:
                #normal user
                session['user_id'] = 2
            resp = c.get('/admin/class')
            self.assertTrue(resp.status_code, 403)



if __name__ == '__main__':
    warnings.warn("Only running app tests.")
    print("To run all tests run 'python test.py'")
    unittest.main()