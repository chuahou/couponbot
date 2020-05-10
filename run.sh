#!/bin/bash
. venv/bin/activate
FLASK_APP=app.py NAME=Test python3 -m flask run
