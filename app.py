from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

if __name__ == '__main__':
    app.run()