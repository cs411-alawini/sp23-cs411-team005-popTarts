from flask import Flask, render_template, request, current_app, redirect, url_for, session
from flask import Blueprint, render_template, send_from_directory
from db import mysql

purchase_bp = Blueprint('purchase', __name__, url_prefix='/purchases')

def bill_info(item): 
    bill_item = {
        'name': item[0],
        'price': item[1],
        'count':item[2],
        'discount': item[3], 
        'id' : item[4]
    }
    return bill_item

@purchase_bp.route('/current')
def current_purchase():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    else: 
        user_id = session['user_id']
        
        
    #will execute transaction and then select 
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.name, i.price, c.count, i.discount, p.productId FROM CartItem c NATURAL JOIN Products p NATURAL JOIN Inventory i WHERE userId = {}".format(user_id))
    cart_items = cur.fetchall()
    cart_items = list(map(bill_info,cart_items))
    return render_template('purchased.html', items=cart_items)



#""" SELECT b.BillId, p.name, b.count, b.cost, p.productId FROM BillItem b NATURAL JOIN Products p WHERE userId = {} ORDER BY b.BillId""".format(user_id))