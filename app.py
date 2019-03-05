from flask import Flask, abort, render_template, url_for, redirect, request, jsonify, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/')
def index():
    return redirect('login')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from models import Users
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username)
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
        if session['user_id'] is not None:
            return redirect('user/' + str(session['user_id']))
        else:
            return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        #bad but gotta avoid circular importss
        from models import Users, Role
        username = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        password = request.form['password']
        password_confirm = request.form['passwordconfirm']
        print(username, first_name, last_name, password)
        #check if username already exists or passsword does not match password confirm
        if (Users.query.filter_by(username=username).count()>0 or password != password_confirm):
            return render_template('create_account.html')
        else:
            role = Role.query.filter_by(name='student').first()
            print(role.id)
            user = Users(username=username, first_name=first_name, last_name=last_name, role_id = role.id)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            db.session.close()
            return redirect('login')
    else:
        return render_template('create_account.html')

@app.route('/user/<int:id>')
def home(id):
    if session['user_id'] is None:
        return redirect(url_for('login', next=request.url))
    elif id != session['user_id']:
        #exit if session user_id isn't the id of the page that user attempted to access
        return abort(401)
    else:
        return "Logged in"

@app.errorhandler(401)
def access_denied(e):
    return "Access Denied"

@app.errorhandler(404)
def page_doesnt_exist(e):
    return "Page doesn't exist."

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'images/favicon.ico')

@app.route('/ajax/username-taken/<string:name>')
def check_username_taken(name):
    #bad but gotta avoid circular importss
    from models import Users
    return jsonify(taken=(Users.query.filter_by(username=name).count()>0))

if __name__ == '__main__':
    app.run()