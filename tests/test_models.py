import os
import sys
sys.path.append("..")
os.environ['APP_SETTINGS'] = 'config.TestingConfig'
os.environ['DATABASE_URL'] = 'postgresql://localhost/gradestest'

import warnings
import unittest
import traceback
import datetime
from app import app, db
from models import Users, Role, Class, GradeFactor, Assignment, AssignmentResult, ClassStudentLink

class TestUsers(unittest.TestCase):
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

class TestWholeClass(unittest.TestCase):
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
        self.user_role = Role(name='user')
        db.session.add(self.user_role)

    def tearDown(self):
        db.session.rollback()


    def test_normal_class(self):
        """test creation of a sample class"""
        #create users of class
        try:
            teacher = Users(username='creswell', first_name='creswell', last_name='creswell', role_id=self.admin_role)
            teacher.set_password('password')
            db.session.add(teacher)
            student1 = Users(username='notcreswell', first_name='notcreswell', last_name='notcreswell', role_id=self.user_role)
            student1.set_password('password')
            db.session.add(student1)
            student2 = Users(username='notcreswell2', first_name='notcreswell2', last_name='notcreswell2', role_id=self.user_role)
            student2.set_password('password')
            db.session.add(student2)
        except:
            self.fail("Failed to create users.")
            traceback.print_exc()
        
        #create class
        try:
            class_ = Class(teacher_id=teacher, join_code="join")
            db.session.add(class_)
        except:
            self.fail("Failed to create class.")
            traceback.print_exc()

        #create gradefactor
        try:
            grade_factor = GradeFactor(class_id=class_, category1_name="tests", category1_weight=0.5, category2_name="quizzes", category2_weight=0.5)
            db.session.add(grade_factor)
        except:
            self.fail("Failed to create grade factor.")
            traceback.print_exc()

        #add students to class
        try:
            class_student_link1 = ClassStudentLink(student_id=student1, class_id=class_)
            db.session.add(class_student_link1)
            class_student_link2 = ClassStudentLink(student_id=student2, class_id=class_)
            db.session.add(class_student_link2)
        except:
            self.fail("Failed to create class student links.")
            traceback.print_exc()

        #add assignments
        try:
            test1 = Assignment(assignment_name="test1", assignment_type=1, assignment_date=datetime.date(2019,1,1), class_id=class_, total_points=100)
            db.session.add(test1)
            quiz1 = Assignment(assignment_name="quiz1", assignment_type=2, assignment_date=datetime.date(2019,1,1), class_id=class_, total_points=50)
            db.session.add(quiz1)
        except:
            self.fail("Failed to create assignments.")
            traceback.print_exc()
        
        #add assignment_results
        try:
            test1_student1 = AssignmentResult(student_id=student1, assignment_id=test1, points_earned=90)
            db.session.add(test1_student1)
            quiz1_student_1 = AssignmentResult(student_id=student1, assignment_id=quiz1, points_earned=45)
            db.session.add(quiz1_student_1)
            test1_student2 = AssignmentResult(student_id=student2, assignment_id=test1, points_earned=80)
            db.session.add(test1_student2)
            quiz1_student_2 = AssignmentResult(student_id=student2, assignment_id=quiz1, points_earned=40)
            db.session.add(quiz1_student_2)
        except:
            self.fail("Failed to create assignment results.")
            traceback.print_exc()
        

if __name__ == '__main__':
    warnings.warn("Only running model tests.")
    print("To run all tests run 'python test.py'")
    unittest.main()