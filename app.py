#!/usr/bin/env python3
from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("base.html", name=os.getenv("NAME", "Invalid Name"))
