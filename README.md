# CreswellGrades

## Install
 
### Install Postgres  
Mac/Windows: [Link](https://www.openscg.com/bigsql/postgresql/installers.jsp/)  
Linux: Install through apt

### Run Application
`export APP_SETTINGS=config.DevelopmentConfig`
`export DATABASE_URL="postgresql://localhost/grades"`
`export SECRET_KEY= ___` (replace with actual secret key)
`export FLASK_APP=app.py`  
`flask run`