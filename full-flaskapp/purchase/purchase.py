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
        'purchaseTime': item[5],
        'totalPrice': item[6],
        
    }
    return bill_item

def purchase_info(item): 
    bill = {
        'billId': item[0],
        'totalPrice': item[1],
        'purchaseTime':item[2],
    }
    return bill

def cart_info(item): 
    cart_item = {
        'itemNumber': item[0],
        'productId':item[2],
        'count': item[3]
    }
    return cart_item

def inventory_info(item):
    intentory_item = {
        'supply': item[0],
        'price': item[1],
        'discount': item[2],
    }
    return intentory_item

@purchase_bp.route('/complete-purchase')
def complete_purchase():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    else: 
        user_id = session['user_id']
    billId = -1 
    #will execute transaction and then select 
    missing_items = False
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * \
                FROM CartItem \
                WHERE CartItem.userId = %s", (user_id,))
    cart_items = cur.fetchall()
    cart_items = list(map(cart_info,cart_items))
    total_price = 0
    inserted = 0
    cur.execute("START TRANSACTION")
    cur.execute('SELECT MAX(billId) FROM Bill'); 
    billId = cur.fetchone()
    if billId[0] == None:
        billId = 0
    else:
        billId = int(billId[0])+1
    cur.execute('INSERT INTO Bill(billId,customerId,totalPrice,purchaseTime) VALUES(%s,%s,%s,CURRENT_TIMESTAMP)',(billId,user_id,0))
    mysql.connection.commit()
    cur.execute("START TRANSACTION")
    for cart_item in cart_items:
        cur.execute("SELECT supply, price, discount FROM Inventory WHERE productId = {}".format(cart_item['productId']))
        inventory_item = cur.fetchone()
        print(inventory_item,cart_item)
        inventory_item = inventory_info(inventory_item)
        print(inventory_item,cart_item)
        if inventory_item['supply']-cart_item['count']>=0:
            inserted+=1
            cur.execute('''DELETE FROM CartItem
                        WHERE productId = %s AND userID = %s;''',
                        (cart_item['productId'],user_id))
            print('billid:',billId)
            cur.execute('INSERT INTO BillItems(billId,count,price,discount,productId) VALUES(%s,%s,%s,%s,%s)',(billId,cart_item['count'],inventory_item['price'],inventory_item['discount'],cart_item['productId']))
            total_price += inventory_item['price']*cart_item['count']*(100-inventory_item['discount'])/100
            cur.execute('UPDATE Inventory SET supply=%s WHERE productId=%s',(inventory_item['supply']-cart_item['count'],cart_item['productId']))
        else:
            missing_items = True
            cur.execute('select * FROM WishList c WHERE c.productId = %s AND c.userId = %s', (cart_item['productId'], user_id))
            exists = cur.fetchone()
            if exists == None:
                cur.execute('SELECT MAX(itemNumber) FROM WishList WHERE userId = %s',(user_id,))
                itemNum = cur.fetchone()
                if itemNum[0] == None:
                    itemNum = 0
                else:
                    current_app.logger.info('retrieve itemnum:{}'.format(itemNum))
                    itemNum = int(itemNum[0])
                cur.execute('INSERT INTO WishList(itemNumber, userId, productId) VALUES (%s,%s,%s)',(itemNum+1,user_id,cart_item['productId']))
            cur.execute('''DELETE FROM CartItem
                        WHERE productId = %s AND userID = %s;''',
                        (cart_item['productId'],user_id))
    if inserted == 0:
        print("ROLLING BACK")
        mysql.connection.rollback()
        cur.execute('DELETE FROM Bill WHERE billId=%s',(billId,))
        mysql.connection.commit()
    else:
        cur.execute('UPDATE Bill SET totalPrice=%s WHERE customerId=%s ORDER BY purchaseTime DESC LIMIT 1',(total_price,user_id))
        mysql.connection.commit()
    
    return redirect("/purchases/view-purchase?bill_id={}".format(billId))

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
                FROM BillItems b NATURAL JOIN Products p NATURAL JOIN Bill bi
                WHERE customerId = {} AND b.billId = {}""".format(user_id,bill_id))
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
    bill = list(map(purchase_info,bill))
    return render_template('all_purchases.html', bill = bill)



#""" SELECT b.BillId, p.name, b.count, b.cost, p.productId FROM BillItem b NATURAL JOIN Products p WHERE userId = {} ORDER BY b.BillId""".format(user_id))