# CreswellGrades

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

### Deploy
`heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro`  
`git push pro master`