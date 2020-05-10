#!/bin/bash
. venv/bin/activate
FLASK_APP=app.py NAME=Test RECIPIENT=Recipient python3 -m flask run
