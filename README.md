# CreswellGrades

## Install
 
### Install Postgres  
Mac/Windows: [Link](https://www.openscg.com/bigsql/postgresql/installers.jsp/)  
Linux: Install through apt

### Run Application
`export DATABASE_URL="postgresql://localhost/grades"`
`export SECRET_KEY= ___` (replace with actual secret key)
`export FLASK_APP=app.py`  
`export FLASK_ENV=development` (development only)  
`flask run`