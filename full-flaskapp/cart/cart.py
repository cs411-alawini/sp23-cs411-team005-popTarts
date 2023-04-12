from flask import Flask, render_template, request, current_app, redirect, url_for, session
from flask import Blueprint, render_template, send_from_directory
from db import mysql

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

def cart_info(item): 
    cart_item = {
        'name': item[0],
        'price': item[1],
        'count':item[2],
    }
    return cart_item
@cart_bp.route('/')
def cart():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    else: 
        user_id = session['user_id']
    
    # Get the user's cart items from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.name, i.price, c.count FROM CartItem c NATURAL JOIN Products p NATURAL JOIN Inventory i WHERE userId = {}".format(user_id))
    cart_items = cur.fetchall()
    cart_items = list(map(cart_info,cart_items))
    return render_template('cart.html', items=cart_items)