#!/usr/bin/env bash

export FLASK_APP=app.py
flask db init
flask db migrate -m "creating databases"
flask db upgrade