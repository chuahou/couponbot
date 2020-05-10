#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Regexp
import psycopg2
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
Bootstrap(app)

name = os.environ["NAME"]
recipient = os.environ["RECIPIENT"]
conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
cursor = conn.cursor()

class CouponForm(FlaskForm):
    code = StringField("Coupon code", validators=[Regexp("[A-Z0-9]{7}")])
    submit = SubmitField("Use Code")

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = CouponForm()
    if form.validate_on_submit():
        return redirect(url_for("submit", code=form.code.data))
    return render_template("index.html", name=name,
            form=form, invalid=(len(form.code.errors) > 0))

@app.route("/submit")
def submit():
    # get records matching our code
    code = request.args.get("code")
    cursor.execute("SELECT offer, used FROM codes WHERE code = '" + code + "'")
    results = cursor.fetchall()

    # error if invalid code or used code
    offer = ""
    error = None
    if (len(results) == 0):
        error = "Invalid code"
    elif (results[0][1]): # used
        error = "Code already used"
    else: # okay
        offer = results[0][0] # get offer text
        cursor.execute( # set offer to used
                "UPDATE codes SET used = true WHERE code = '" + code + "'")
        conn.commit()

    # return template
    return render_template("submit.html", name=name, recipient=recipient,
            code=code, offer=offer, error=error, success=(error == None))

