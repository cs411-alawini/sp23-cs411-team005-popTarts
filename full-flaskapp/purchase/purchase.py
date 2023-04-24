from flask import Flask, render_template, request, current_app, redirect, url_for, session
from flask import Blueprint, render_template, send_from_directory
from db import mysql

purchase_bp = Blueprint('purchase', __name__, url_prefix='/purchase-complete')

def bill_info(item): 
    bill_item = {
        'name': item[0],
        'price': item[1],
        'count':item[2],
        'discount': item[3], 
        'id' : item[4]
    }
    return bill_item

@purchase_bp.route('/')
def cart():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    else: 
        user_id = session['user_id']
    
    # Get the user's cart items from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.name, i.price, c.count, i.discount, p.productId FROM CartItem c NATURAL JOIN Products p NATURAL JOIN Inventory i WHERE userId = {}".format(user_id))
    cart_items = cur.fetchall()
    cart_items = list(map(bill_info,cart_items))
    return render_template('purchased.html', items=cart_items)