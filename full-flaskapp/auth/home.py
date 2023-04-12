from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('products.get_search_term'))
    else:
        return redirect(url_for('login.login'))