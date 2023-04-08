from flask import Blueprint, render_template, redirect, url_for, request, session
from db import mysql

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']


        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM User WHERE username = %s', [username])
        user = cur.fetchone()

        if user is None:

            cur.execute('INSERT INTO Customers (firstName, lastName, username) VALUES (%s, %s, %s)', (first_name, last_name, username))
            mysql.connection.commit()
            session['user_id'] = cur.lastrowid

            cur.execute('INSERT INTO User (username, password, userId) VALUES (%s, %s, %s)', (username, password, session['user_id']))
            mysql.connection.commit()


            session['username'] = username


            return redirect(url_for('home.home'))
        else:

            error = 'Username already taken'


        return render_template('register.html', error=error)
    else:
        return render_template('register.html')

