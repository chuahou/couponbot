#!/usr/bin/env python3
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
Bootstrap(app)

class Form(FlaskForm):
    code = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Use Code")

@app.route("/")
def index():
    return render_template("base.html", name=os.getenv("NAME", "Invalid Name"),
            form=Form())
