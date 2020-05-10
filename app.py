#!/usr/bin/env python3

# flask imports and extensions
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Regexp

# PostgreSQL
import psycopg2

# standard imports
import os # environ
import requests # sending email

# main app setup
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
Bootstrap(app)

# get environment variables
NAME = os.environ["NAME"]
RECIPIENT = os.environ["RECIPIENT"]
DATABASE_URL = os.environ["DATABASE_URL"]
MAILGUN_API_KEY = os.environ["MAILGUN_API_KEY"]
MAILGUN_DOMAIN = os.environ["MAILGUN_DOMAIN"]
MAILGUN_FROM = os.environ["MAILGUN_FROM"]
MAILGUN_TO = os.environ["MAILGUN_TO"]
MAILGUN_SUBJECT = os.environ["MAILGUN_SUBJECT"]

# main coupon submission form
# only accepts uppercase alpha numeric input of length 7
class CouponForm(FlaskForm):
    code = StringField("Coupon code", validators=[Regexp("[A-Z0-9]{7}")])
    submit = SubmitField("Use Code")

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = CouponForm()
    if form.validate_on_submit():
        return redirect(url_for("submit", code=form.code.data))
    return render_template("index.html", name=NAME,
            form=form, invalid=(len(form.code.errors) > 0))

@app.route("/submit")
def submit():
    # stores error message
    error = None

    # stores retrieved offer
    offer = ""

    try:
        # connect to database
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()

        # get records matching our code
        code = request.args.get("code")
        cursor.execute(
                "SELECT offer, used FROM codes WHERE code = '" + code + "'")
        results = cursor.fetchall()

        # error if invalid code or used code
        if (len(results) == 0):
            error = "Invalid code"
        elif (results[0][1]): # used
            error = "Code already used"
        else: # okay
            offer = results[0][0] # get offer text
            cursor.execute( # set offer to used
                    "UPDATE codes SET used = true WHERE code = '" + code + "'")
            conn.commit()
            requests.post(
                f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
                auth=("api", MAILGUN_API_KEY),
                data={"from": MAILGUN_FROM,
                      "to": [MAILGUN_TO],
                      "subject": MAILGUN_SUBJECT,
                      "text": f"Code: {code}, Offer: {offer} claimed"})
    except (Exception, psycopg2.Error) as error:
        error = "Database connection error"
    finally:
        # close connection
        if (conn):
            cursor.close()
            conn.close()

    # return template
    return render_template("submit.html", name=NAME, recipient=RECIPIENT,
            code=code, offer=offer, error=error, success=(error is None))

