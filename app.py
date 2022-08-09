from email.policy import default
from urllib import request
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
app.config['SECRET_KEY'] = 'SomethingSecret'

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    send_date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/', methods=['POST'])
def submit_form():

    new_contact = Contact(
        name=request.form['name'],
        email=request.form['email'],
        message=request.form['message'])

    try:
        db.session.add(new_contact)
        db.session.commit()
        flash('Message sent successfully', 'success')

        return redirect(url_for('submit_form', _anchor='contact'))

    except:
        return flash("Please enter a valid email address", 'danger')
