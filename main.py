import json
import smtplib

from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap5
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
Bootstrap5(app)

now = datetime.now()
current_year = now.year


class contactForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired()])
    message = TextAreaField('Message', [validators.InputRequired()])
    submit = SubmitField('Send')


my_email = "my email"
my_pwd = "my email password"

try:
    with open("data.json", "r") as data_file:
        data = json.load(data_file)

except FileNotFoundError:
    print("Error, file not located.")
except json.decoder.JSONDecodeError:
    print("Error, file empty.")
else:
    my_email = data["gmail"]["email"]
    my_pwd = data["gmail"]["password"]


@app.route("/")
def home():
    return render_template('index.html', year=current_year)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    cForm = contactForm()
    try:
        if cForm.validate_on_submit():
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_pwd)
                connection.sendmail(
                    from_addr=cForm.email.data,
                    to_addrs=my_email,
                    msg=f"Subject: Portfolio contact form \n\nName: {cForm.name.data},\n\nEmail: {cForm.email.data}, \n\n{cForm.message.data}")
            cForm = contactForm(formdata=None)
            flash("Thank you. Message sent successfully.")
    except UnicodeEncodeError:
        flash("Sorry emoji's not supported. Message not sent.")
        return render_template('contact.html', form=cForm, year=current_year)
    else:
        return render_template('contact.html', form=cForm, year=current_year)


@app.route("/resume")
def resume():
    return render_template('resume.html', year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
