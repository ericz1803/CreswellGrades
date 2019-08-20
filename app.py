from flask import Flask, abort, flash, render_template, url_for, redirect, request, jsonify, send_from_directory, session
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from flask_wtf.csrf import CSRFProtect, CSRFError
from wtforms import PasswordField
from flask_mail import Mail, Message
from flask_session import Session
import flask_bcrypt
import string
import random
import secrets
from functools import wraps
from collections import defaultdict

#init
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

import models

csrf = CSRFProtect()
csrf.init_app(app)
mail = Mail(app)

if not app.config['DEBUG']:
    sess = Session()
    sess.init_app(app)

#admin interface
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        #true if role_id is admin
        try:
            allowed = (models.Users.query.filter_by(id=session['user_id']).first().role_id == 1)
            return (allowed)
        except:
            return False
    
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if 'user_id' in session.keys():
                abort(403)
            else:
                return redirect(url_for('login', next=request.url))

class MyModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        #true if role_id is admin
        try:
            allowed = (models.Users.query.filter_by(id=session['user_id']).first().role_id == 1)
            return (allowed)
        except:
            return False
    
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if 'user_id' in session.keys():
                abort(403)
            else:
                return redirect(url_for('login', next=request.url))

class UserView(ModelView):
    column_display_pk = True
    column_exclude_list = ('password_hash',)
    form_excluded_columns = ('password_hash',)
    form_extra_fields = {
        'password': PasswordField('password')
    }

    def is_accessible(self):
        #true if role_id is admin
        try:
            allowed = (models.Users.query.filter_by(id=session['user_id']).first().role_id == 1)
            return (allowed)
        except:
            return False
    
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if 'user_id' in session.keys():
                abort(403)
            else:
                return redirect(url_for('login', next=request.url))

    def on_model_change(self, form, user, is_created):
        if form.password.data is not None:
            user.set_password(form.password.data)

admin = Admin(app, name="admin", template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(UserView(models.Users, db.session))
admin.add_view(MyModelView(models.Role, db.session))
admin.add_view(MyModelView(models.Class, db.session))
admin.add_view(MyModelView(models.GradeFactor, db.session))
admin.add_view(MyModelView(models.GradeScale, db.session))
admin.add_view(MyModelView(models.Assignment, db.session))
admin.add_view(MyModelView(models.AssignmentResult, db.session))
admin.add_view(MyModelView(models.ClassStudentLink, db.session))
admin.add_link(MenuLink(name='Logout', category='', url='/logout'))

#just checks that a user is logged in
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))

        return f(*args, **kwargs)
    return wrap

#checks if logged in user is a teacher
def teacher_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user = models.Users.query.filter_by(id=session['user_id']).first_or_404()
        if user.role_id != 3:
            return abort(403)

        return f(*args, **kwargs)
    return wrap

#checks if logged in user is a student
def student_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user = models.Users.query.filter_by(id=session['user_id']).first_or_404()
        if user.role_id != 2:
            return abort(403)

        return f(*args, **kwargs)
    return wrap

@app.route('/')
def index():
    return redirect('/login')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = models.Users.query.filter_by(username=username)
        if user.count() == 1:
            user = user.first()
        else:
            print("Username " + username + " does not exist.")
            flash('Incorrect username or password.')
            return redirect('/login')
        
        if user.check_password(password):
            session['user_id'] = user.id
            session['secret_key'] = secrets.token_hex(32)
            return redirect('user/' + str(session['user_id']))
        else:
            print("Incorrect password.")
            flash('Incorrect username or password.')
            return redirect('/login')
    else:
        #do not let them login if user_id already exists
        if 'user_id' in session.keys():
            return redirect('/user/' + str(session['user_id']))
        else:
            return render_template('login.html')


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        user = models.Users.query.filter_by(email=email).first()
        if not user:
            return abort(415)

        msg = Message('Reset password.', recipients=[email])
        #generate random string
        reset_link = ''.join(random.choices(string.ascii_letters + string.digits, k=60))
        user.password_reset = reset_link
        db.session.commit()
        db.session.close()
        msg.body = f"Hi {user.username},\n\nUse this link to reset your password:\nhttps://creswell-grades.herokuapp.com/reset/{reset_link}"
        with app.app_context():
            mail.send(msg)
            print("SENT")
        return redirect('/login')
    else:
        return render_template('forgot.html')

@app.route('/reset/<reset>', methods=['GET','POST'])
def reset(reset):
    if request.method == 'POST':
        user = models.Users.query.filter_by(password_reset=reset).first_or_404()
        user.set_password(request.form['password'])
        user.password_reset = None
        db.session.commit()
        db.session.close()
        return redirect('/login')
    else:
        print(reset)
        user = models.Users.query.filter_by(password_reset=reset).first_or_404()
        return render_template('reset.html', username=user.username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        password = request.form['password']
        password_confirm = request.form['passwordconfirm']
        email = request.form.get('email')
        #check if username already exists or password does not match password confirm
        if (models.Users.query.filter_by(username=username).count()>0 or password != password_confirm):
            return render_template('create_account.html')
        else:
            role = models.Role.query.filter_by(name='student').first()
            user = models.Users(username=username, first_name=first_name, last_name=last_name, email=email, role_id=role.id)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            db.session.close()
            return redirect('/login')
    else:
        return render_template('create_account.html')

@app.route('/create-teacher', methods=['GET', 'POST'])
def create_teacher_account():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        password = request.form['password']
        password_confirm = request.form['passwordconfirm']
        email = request.form.get('email')
        #check if username already exists or password does not match password confirm
        if (models.Users.query.filter_by(username=username).count()>0 or password != password_confirm):
            return render_template('create_account.html')
        else:
            role = models.Role.query.filter_by(name='teacher').first()
            user = models.Users(username=username, first_name=first_name, last_name=last_name, email=email, role_id=role.id)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            db.session.close()
            return redirect('/login')
    else:
        return render_template('create_account.html')

@app.route('/user/<int:id>')
@login_required
def home(id):
    if id != session['user_id']:
        #exit if session user_id isn't the id of the page that user attempted to access
        return abort(403)
    else:
        #return user interface if not admin else admin interface
        user = models.Users.query.filter_by(id=session['user_id']).first_or_404()
        if user.role_id == 1:
            return redirect('/admin')
        elif user.role_id == 3:
            #teacher
            classes = models.Class.query.filter_by(teacher_id=session['user_id'])
            return render_template('teacher_home.html', classes=classes)
        else:
            #classes that student is enrolled in
            try:
                classes, _, _ = zip(*(db.session.query(models.Class, models.Users, models.ClassStudentLink)
                .join(models.ClassStudentLink, models.Class.id == models.ClassStudentLink.class_id)
                .join(models.Users, models.Users.id == models.ClassStudentLink.student_id)
                .filter(models.Users.id==session['user_id']).all()))
                return render_template('student_home.html', classes=classes)
            except:
                return render_template('student_home.html')

@app.route('/create-class', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_class():
    if request.method == 'POST':
        class_name = request.form['class_name']
        join_code = request.form['join_code']
        user_id = session['user_id']
        a = request.form['a']
        b = request.form['b']
        c = request.form['c']
        d = request.form['d']

        cat1name = request.form['category_name1']
        cat1val = request.form['category_value1']
        cat1drop = request.form.get('category_drop1')
        cat2name = request.form.get('category_name2')
        cat2val = request.form.get('category_value2')
        cat2drop = request.form.get('category_drop2')
        cat3name = request.form.get('category_name3')
        cat3val = request.form.get('category_value3')
        cat3drop = request.form.get('category_drop3')
        cat4name = request.form.get('category_name4')
        cat4val = request.form.get('category_value4')
        cat4drop = request.form.get('category_drop4')
        cat5name = request.form.get('category_name5')
        cat5val = request.form.get('category_value5')
        cat5drop = request.form.get('category_drop5')
        cat6name = request.form.get('category_name6')
        cat6val = request.form.get('category_value6')
        cat6drop = request.form.get('category_drop6')
        cat7name = request.form.get('category_name7')
        cat7val = request.form.get('category_value7')
        cat7drop = request.form.get('category_drop7')
        cat8name = request.form.get('category_name8')
        cat8val = request.form.get('category_value8')
        cat8drop = request.form.get('category_drop8')

        new_class = models.Class(teacher_id=user_id, name=class_name, join_code=join_code)
        new_grade_factor = models.GradeFactor(
            category1_name = cat1name,
            category1_weight = cat1val,
            category1_drop = cat1drop,
            category2_name = cat2name,
            category2_weight = cat2val,
            category2_drop = cat2drop,
            category3_name = cat3name,
            category3_weight = cat3val,
            category3_drop = cat3drop,
            category4_name = cat4name,
            category4_weight = cat4val,
            category4_drop = cat4drop,
            category5_name = cat5name,
            category5_weight = cat5val,
            category5_drop = cat5drop,
            category6_name = cat6name,
            category6_weight = cat6val,
            category6_drop = cat6drop,
            category7_name = cat7name,
            category7_weight = cat7val,
            category7_drop = cat7drop,
            category8_name = cat8name,
            category8_weight = cat8val,
            category8_drop = cat8drop,
            class_id=new_class.id,
            class_=new_class
        )
        new_grade_scale = models.GradeScale(a_b=a, b_c=b, c_d=c, d_f=d, class_id=new_class.id, class_=new_class)
        db.session.add(new_class)
        db.session.add(new_grade_factor)
        db.session.add(new_grade_scale)
        db.session.commit()
        db.session.close()
        return redirect('/')
    else:
        return render_template('create_class.html')

@app.route('/class/<int:id>')
@login_required
@teacher_required
def teacher_class(id):
    #check that the right teacher is accessing it
    if models.Class.query.filter_by(id=id).first_or_404().teacher_id != session['user_id']:
        return abort(403)

    return redirect('/class/grades/' + str(id))

@app.route('/class/about/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_class_about(id):
    #check that the right teacher is accessing it
    if models.Class.query.filter_by(id=id).first_or_404().teacher_id != session['user_id']:
        return abort(403)

    if request.method == 'POST':
        #update class obj
        class_obj = models.Class.query.filter_by(id=id).first_or_404()
        class_obj.name = request.form['class_name']
        class_obj.join_code = request.form['join_code']
        
        #update grade scale
        grade_scale = models.GradeScale.query.filter_by(class_id=id).first_or_404()
        grade_scale.a_b = request.form['a']
        grade_scale.b_c = request.form['b']
        grade_scale.c_d = request.form['c']
        grade_scale.d_f = request.form['d']
        
        #update grade factor
        grade_factor = models.GradeFactor.query.filter_by(class_id=id).first_or_404()
        grade_factor.category1_name = request.form['category_name1']
        grade_factor.category1_weight = request.form['category_value1']
        grade_factor.category1_drop = request.form['category_drop1']
        grade_factor.category2_name = request.form.get('category_name2')
        grade_factor.category2_weight = request.form.get('category_value2')
        grade_factor.category2_drop = request.form.get('category_drop2')
        grade_factor.category3_name = request.form.get('category_name3')
        grade_factor.category3_weight = request.form.get('category_value3')
        grade_factor.category3_drop = request.form.get('category_drop3')
        grade_factor.category4_name = request.form.get('category_name4')
        grade_factor.category4_weight = request.form.get('category_value4')
        grade_factor.category4_drop = request.form.get('category_drop4')
        grade_factor.category5_name = request.form.get('category_name5')
        grade_factor.category5_weight = request.form.get('category_value5')
        grade_factor.category5_drop = request.form.get('category_drop5')
        grade_factor.category6_name = request.form.get('category_name6')
        grade_factor.category6_weight = request.form.get('category_value6')
        grade_factor.category6_drop = request.form.get('category_drop6')
        grade_factor.category7_name = request.form.get('category_name7')
        grade_factor.category7_weight = request.form.get('category_value7')
        grade_factor.category7_drop = request.form.get('category_drop7')
        grade_factor.category8_name = request.form.get('category_name8')
        grade_factor.category8_weight = request.form.get('category_value8')
        grade_factor.category8_drop = request.form.get('category_drop8')
        db.session.commit()
        db.session.close()

        return redirect(f'/class/about/{id}')
    else:
        class_obj = models.Class.query.filter_by(id=id).first_or_404()
        grade_scale = models.GradeScale.query.filter_by(class_id=id).first_or_404()
        grade_factor = models.GradeFactor.query.filter_by(class_id=id).first_or_404()
        return render_template('teacher_class_about.html', class_obj=class_obj, grade_scale=grade_scale, grade_factor=grade_factor)

@app.route('/class/grades/<int:id>')
@login_required
@teacher_required
def teacher_class_grades(id):
    #check that the right teacher is accessing it
    if models.Class.query.filter_by(id=id).first_or_404().teacher_id != session['user_id']:
        return abort(403)
        
    class_obj = models.Class.query.filter_by(id=id).first_or_404()
    grade_scale = models.GradeScale.query.filter_by(class_id=id).first_or_404()
    grade_factor = models.GradeFactor.query.filter_by(class_id=id).first_or_404()
    
    assignments = models.Assignment.query.filter_by(class_id=id).order_by(models.Assignment.assignment_type, models.Assignment.assignment_date, models.Assignment.id).all()
    #print(assignments)
    students = db.session.query(models.Users, models.ClassStudentLink) \
                .join(models.ClassStudentLink, models.ClassStudentLink.student_id == models.Users.id) \
                .filter(models.ClassStudentLink.class_id==id).all()
    if students:
        students, _ = zip(*(students))
    #print(students)
    assignment_results = db.session.query(models.Assignment, models.Class, models.AssignmentResult) \
                        .join(models.Class, models.Assignment.class_id == models.Class.id) \
                        .join(models.AssignmentResult, models.Assignment.id == models.AssignmentResult.assignment_id) \
                        .filter(models.Class.id == id).order_by(models.AssignmentResult.student_id).all()
    if assignment_results:
        _, _, assignment_results = zip(*(assignment_results))
    assignment_results_dict = defaultdict(list)
    for assignment_result in assignment_results:
        assignment_results_dict[assignment_result.student_id].append(assignment_result)

    #print(assignment_results, assignment_results_dict.items())
    return render_template('teacher_class_grades.html', students=list(students), class_obj=class_obj,
           assignments=assignments, grade_factor=grade_factor, assignment_results=assignment_results_dict,
           grade_scale=grade_scale, secret_key=session['secret_key'])

@app.route('/join', methods=['GET', 'POST'])
@login_required
@student_required
def join():
    if request.method == 'POST':
        join_code = request.form['join_code']
        class_ = models.Class.query.filter_by(join_code=join_code).first()
        if not class_:
            return "Class not found"
        else:
            new_class_student_link = models.ClassStudentLink(student_id=session['user_id'], class_id=class_.id)
            db.session.add(new_class_student_link)
            db.session.commit()
            db.session.close()
            return redirect('/')
    else:
        return render_template('join.html')

@app.route('/classes/<int:id>')
@login_required
@student_required
def classes(id):
    #check that user is in that class
    _ = models.ClassStudentLink.query.filter_by(student_id=session['user_id'], class_id=id).first_or_404()
    
    class_obj = models.Class.query.filter_by(id=id).first_or_404()
    
    assignments = models.Assignment.query.filter_by(class_id=id).order_by(models.Assignment.assignment_type, models.Assignment.assignment_date, models.Assignment.id).all()

    grade_factor = models.GradeFactor.query.filter_by(class_id=id).first_or_404()
    grade_scale = models.GradeScale.query.filter_by(class_id=id).first_or_404()

    query = db.session.query(models.Assignment, models.Class, models.AssignmentResult) \
                        .join(models.Class, models.Assignment.class_id == models.Class.id) \
                        .join(models.AssignmentResult, models.Assignment.id == models.AssignmentResult.assignment_id) \
                        .filter(models.Class.id == id, models.AssignmentResult.student_id == session['user_id']) \
                        .order_by(models.Assignment.assignment_type, models.Assignment.assignment_date, models.Assignment.id).all()
    grades = defaultdict(list)
    """
        format:
        {
            1: [(assignment, result), (assignment, result)],
            2: [(assignment, result), (assignment, result)]
        }
    """
    for assignment in assignments:
        #get result if exists
        result = next((r for a, c, r in query if a == assignment), None)
        
        grades[assignment.assignment_type].append((assignment, result))
    return render_template('student_grades.html', grades=grades, grade_factor=grade_factor, grade_scale=grade_scale, class_obj=class_obj)

@app.route('/ajax/update-grades', methods=['GET', 'POST'])
@login_required
@teacher_required
def update_grades():
    if request.method == 'POST' and request.headers['secret_key'] == session['secret_key']:
        print(request.json)

        assignment = models.Assignment.query.get_or_404(request.json['assignment_id'])
        assignment.assignment_name = request.json['name']
        assignment.assignment_type = request.json['category']
        assignment.assignment_date = request.json['date']
        assignment.total_points = request.json['points']
        for (student_id, points) in request.json['student_points']:
            result = models.AssignmentResult.query.filter_by(assignment_id=assignment.id, student_id=student_id).all()
            if result and points is not None:
                result[0].student_id = student_id
                result[0].points_earned = points
            elif not result and points is not None:
                new_result = models.AssignmentResult(student_id=student_id, assignment_id=assignment.id, points_earned=points)
                db.session.add(new_result)
            elif result and points is None:
                db.session.delete(result[0])

        db.session.commit()
        db.session.close()
        return jsonify(saved=True)
    else:
        return jsonify(saved=False)

@app.route('/ajax/new-grades', methods=['GET', 'POST'])
@login_required
@teacher_required
def new_grades():
    if request.method == 'POST' and request.headers['secret_key'] == session['secret_key']:
        print(request.json)
        
        new_assignment = models.Assignment(assignment_name=request.json['name'], assignment_type=request.json['category'], \
                         assignment_date=request.json['date'], total_points=request.json['points'], class_id=request.json['id'])
        db.session.add(new_assignment)
        print(request.json['student_points'])
        for (student_id, points) in request.json['student_points'].items():
            if points is not None:
                result = models.AssignmentResult.query.filter_by(assignment_id=new_assignment.id, student_id=student_id).all()
                if result:
                    result[0].student_id = student_id
                    result[0].points_earned = points
                else:
                    new_result = models.AssignmentResult(student_id=student_id, assignment_id=new_assignment.id, points_earned=points)
                    db.session.add(new_result)
        
        db.session.commit()
        db.session.close()

        #get assignment id for adding it to list
        new_id = models.Assignment.query.filter_by(assignment_name=request.json['name']).first_or_404().id
        print(new_id)
        return jsonify(saved=True, id=new_id)
    else:
        return jsonify(saved=False)

@app.route('/ajax/username-taken/<string:name>')
def check_username_taken(name):
    return jsonify(taken=(models.Users.query.filter_by(username=name).count()>0))

@app.errorhandler(403)
def access_denied(e):
    context = {'error_num': 403,
               'error_name': 'Forbidden',
               'description': 'Access Denied.'
               }
    return render_template('error.html', context=context), 403

@app.errorhandler(404)
def page_doesnt_exist(e):
    context = {'error_num': 404,
               'error_name': 'Not Found',
               'description': 'Page Not Found.'
               }
    return render_template('error.html', context=context), 404

@app.errorhandler(415)
def user_not_found(e):
    context = {'error_num': 415,
               'error_name': 'User Not Found',
               'description': 'User with that email address not found.'
               }
    return render_template('error.html', context=context), 415

@app.errorhandler(500)
def internal_server_error(e):
    context = {'error_num': 500,
               'error_name': 'Internal Server Error',
               'description': 'Internal Server Error.'
               }
    return render_template('error.html', context=context), 500

@app.errorhandler(CSRFError)
def csrf_error(e):
    context = {'error_num': 400,
               'error_name': 'CSRF Error',
               'description': e.description
               }
    return render_template('error.html', context=context), 400

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'images/favicon.ico')



if __name__ == '__main__':
    app.run()