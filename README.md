# [CreswellGrades](https://creswell-grades.herokuapp.com/)

## Install
 
### Install Postgres  
Mac/Windows: [Link](https://www.openscg.com/bigsql/postgresql/installers.jsp/)  
Linux: Install through apt

### Create Postgres Databases
`psql -U postgres`  
`CREATE DATABASE grades`  
`CREATE DATABASE gradestest` (for testing)  

### First Time Setup
`pip install pipenv`  
`pipenv install`  
`pipenv shell` (run everything in virtual environment)  

### Run Application
`export APP_SETTINGS=config.DevelopmentConfig`  
`export DATABASE_URL="postgresql://localhost/grades"`  
`export SECRET_KEY= ___` (replace with actual secret key)  
`export FLASK_APP=app.py`  
`flask run`

### Edit Models
1. Make edits in models.py.
2. (first time) `python manage.py db init`
3. (first time) `python set_up_db.py`
4. `python manage.py db migrate`
5. `python manage.py db upgrade`

### Deploy
`heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro`  
`git push pro master`
