from flask import Blueprint, render_template, redirect, url_for, request, session, current_app, flash 
from db import mysql

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info('in')
    if request.method == 'POST':
        current_app.logger.info('in post')
        username = request.form['username']
        password = request.form['password']


        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM User WHERE username = %s', [username])
        user = cur.fetchone()

        if user is not None:
            if password == user[1]:
                session['user_id'] = user[2]
                session['username'] = user[0]
                return redirect(url_for('home.home'))
            else:
                flash('Invalid email or password', 'error')
        else:
            flash('Invalid email or password', 'error')
        return render_template('login.html')
    else:
        return render_template('login.html')
