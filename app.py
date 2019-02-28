from flask import Flask, render_template, url_for, redirect, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

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
        return "Post request received"
    else:
        return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        return "Post request received"
    else:
        return render_template('create_account.html')

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