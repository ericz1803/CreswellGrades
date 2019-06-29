#!/bin/bash

export APP_SETTINGS=config.DevelopmentConfig
export DATABASE_URL="postgresql://localhost/grades"
export FLASK_APP=app.py
flask run