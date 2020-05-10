#!/usr/bin/env python3
from flask import Flask, render_template, redirect, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
Bootstrap(app)

name = os.getenv("NAME", "Invalid Name")
recipient = os.getenv("RECIPIENT", "Invalid Recipient")

class CouponForm(FlaskForm):
    code = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Use Code")

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = CouponForm()
    if form.validate_on_submit():
        flash(f"Code submitted: {form.code.data}")
        return redirect("/submit")
    return render_template("index.html", name=name,
            form=form, invalid=(len(form.code.errors) > 0))

@app.route("/submit")
def submit():
    return render_template("submit.html", name=name, recipient=recipient,
            code="ASKDJ", offer="Offer")

