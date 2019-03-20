from flask import Flask, abort, render_template, url_for, redirect, request, jsonify, send_from_directory, session
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
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
admin.add_view(MyModelView(models.Assignment, db.session))
admin.add_view(MyModelView(models.AssignmentResult, db.session))
admin.add_view(MyModelView(models.ClassStudentLink, db.session))



@app.route('/')
def index():
    return redirect('login')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear() #remove line later
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = models.Users.query.filter_by(username=username)
        if user.count() == 1:
            user = user.first()
        else:
            print("Username " + username + " does not exist.")
            return redirect('login')
        
        if user.check_password(password):
            session['user_id'] = user.id
            return redirect('user/' + str(user.id))
        else:
            print("Incorrect password.")
            return redirect('login')
    else:
        #do not let them login if user_id already exists
        if 'user_id' in session.keys():
            return redirect('user/' + str(session['user_id']))
        else:
            return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        #bad but gotta avoid circular importss
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

@app.route('/user/<int:id>')
def home(id):
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.url))
    elif id != session['user_id']:
        #exit if session user_id isn't the id of the page that user attempted to access
        return abort(403)
    else:
        #return user interface if not admin else admin interface
        user = models.Users.query.filter_by(id=session['user_id']).first()
        if not user:
            abort(404)
        elif user.role_id == 1:
            return redirect('admin')
        else:
            return "Normal User"
 
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