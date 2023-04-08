from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('login.login'))