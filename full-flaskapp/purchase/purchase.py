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
        'id' : item[4],
        'purchaseTime': item[5]
    }
    return bill_item
def purchase_info(item): 
    bill = {
        'billId': item[0],
        'totalPrice': item[1],
        'purchaseTime':item[2],
    }
    return bill

@purchase_bp.route('/complete-purchase')
def complete_purchase():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    else: 
        user_id = session['user_id']
        
        
    #will execute transaction and then select 
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.name, i.price, c.count, i.discount, p.productId FROM CartItem c NATURAL JOIN Products p NATURAL JOIN Inventory i WHERE userId = {}".format(user_id))
    cart_items = cur.fetchall()
    cart_items = list(map(bill_info,cart_items))
    return render_template('complete_purchase.html', items=cart_items)

@purchase_bp.route('/view-purchase')
def view_purchase():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    else: 
        user_id = session['user_id']
        
    bill_id = request.args.get('bill_id')
    
        
    #will execute transaction and then select 
    
    cur = mysql.connection.cursor()
    cur.execute("""SELECT p.name, b.price, b.count, b.discount, p.productId, bi.purchaseTime, bi.totalPrice
                FROM BillItem b NATURAL JOIN Products p NATURAL JOIN Bill bi
                WHERE userId = {} AND b.billId = %s""".format(user_id), (bill_id))
    bill_items = cur.fetchall()
    bill_items = list(map(bill_info,bill_items))
    return render_template('view_purchase.html', items=bill_items)

@purchase_bp.route('/all-purchases')
def all_purchases():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    else: 
        user_id = session['user_id']
        
        
    #will execute transaction and then select 
    
    cur = mysql.connection.cursor()
    cur.execute("""SELECT b.billId, b.totalPrice, b.purchaseTime FROM Bill b
                WHERE customerId = {} ORDER BY b.purchaseTime DESC""".format(user_id))
    bill = cur.fetchall()
    bill = list(map(bill_info,bill))
    return render_template('all_purchases.html', bill = bill)



#""" SELECT b.BillId, p.name, b.count, b.cost, p.productId FROM BillItem b NATURAL JOIN Products p WHERE userId = {} ORDER BY b.BillId""".format(user_id))