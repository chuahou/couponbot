#!/usr/bin/env python3
from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def hello_world():
    return f"Hello, {os.getenv('NAME', default='Name')}!"
