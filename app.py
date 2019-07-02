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

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

import models

csrf = CSRFProtect()
csrf.init_app(app)

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


@app.route('/')
def index():
    return redirect('login')
    
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
            return redirect('login')
        
        if user.check_password(password):
            session['user_id'] = user.id
            return redirect('/')
        else:
            print("Incorrect password.")
            flash('Incorrect username or password.')
            return redirect('login')
    else:
        #do not let them login if user_id already exists
        if 'user_id' in session.keys():
            return redirect('user/' + str(session['user_id']))
        else:
            return render_template('login.html')

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
        #check if username already exists or password does not match password confirm
        if (models.Users.query.filter_by(username=username).count()>0 or password != password_confirm):
            return render_template('create_account.html')
        else:
            role = models.Role.query.filter_by(name='student').first()
            user = models.Users(username=username, first_name=first_name, last_name=last_name, role_id = role.id)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            db.session.close()
            return redirect('login')
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
        #check if username already exists or password does not match password confirm
        if (models.Users.query.filter_by(username=username).count()>0 or password != password_confirm):
            return render_template('create_account.html')
        else:
            role = models.Role.query.filter_by(name='teacher').first()
            user = models.Users(username=username, first_name=first_name, last_name=last_name, role_id = role.id)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            db.session.close()
            return redirect('login')
    else:
        return render_template('create_account.html')

@app.route('/user/<int:id>')
def home(id):
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.url))
    elif id != session['user_id']:
        #exit if session user_id isn't the id of the page that user attempted to access
        return abort(403)
    else:
        #return user interface if not admin else admin interface
        user = models.Users.query.filter_by(id=session['user_id']).first_or_404()
        if user.role_id == 1:
            return redirect('admin')
        elif user.role_id == 3:
            #teacher
            classes = models.Class.query.filter_by(teacher_id=session['user_id'])
            return render_template('teacher_home.html', classes=classes)
        else:
            #student
            classes = models.ClassStudentLink.query.filter_by(student_id=session['user_id'])
            context = {classes:zip(classes, [class_.id for class_ in classes])}
            return render_template('student_home.html', context=context)
 
@app.route('/join', methods=['GET', 'POST'])
def join():
    #check user is logged in first
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.url))
    else:
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

@app.route('/create-class', methods=['GET', 'POST'])
def create_class():
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.url))
    else:
        user = models.Users.query.filter_by(id=session['user_id']).first_or_404()
        #check that user is teacher
        if user.role_id != 3:
            return abort(403)
        else:
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
                cat2name = request.form.get('category_name2')
                cat2val = request.form.get('category_value2')
                cat3name = request.form.get('category_name3')
                cat3val = request.form.get('category_value3')
                cat4name = request.form.get('category_name4')
                cat4val = request.form.get('category_value4')
                cat5name = request.form.get('category_name5')
                cat5val = request.form.get('category_value5')
                cat6name = request.form.get('category_name6')
                cat6val = request.form.get('category_value6')
                cat7name = request.form.get('category_name7')
                cat7val = request.form.get('category_value7')
                cat8name = request.form.get('category_name8')
                cat8val = request.form.get('category_value8')

                new_class = models.Class(teacher_id=user_id, name=class_name, join_code=join_code)
                new_grade_factor = models.GradeFactor(
                    category1_name = cat1name,
                    category1_weight = cat1val,
                    category2_name = cat2name,
                    category2_weight = cat2val,
                    category3_name = cat3name,
                    category3_weight = cat3val,
                    category4_name = cat4name,
                    category4_weight = cat4val,
                    category5_name = cat5name,
                    category5_weight = cat5val,
                    category6_name = cat6name,
                    category6_weight = cat6val,
                    category7_name = cat7name,
                    category7_weight = cat7val,
                    category8_name = cat8name,
                    category8_weight = cat8val,
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
def teacher_class(id):
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.url))
    else:
        user = models.Users.query.filter_by(id=session['user_id']).first_or_404()
        #check that user is teacher
        if user.role_id != 3:
            return abort(403)
        else:
            class_obj = models.Class.query.filter_by(id=id).first_or_404()
            return render_template('teacher_class.html', class_obj=class_obj)

@app.route('/classes/<int:id>')
def classes(id):
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.url))
    else:
        #check that user is in that class
        student_in_class = models.ClassStudentLink.query.filter_by(student_id=session['user_id'], class_id=id).first_or_404()
        return "grades"

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

@app.route('/ajax/username-taken/<string:name>')
def check_username_taken(name):
    return jsonify(taken=(models.Users.query.filter_by(username=name).count()>0))

if __name__ == '__main__':
    app.run()