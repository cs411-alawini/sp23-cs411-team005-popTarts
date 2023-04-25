from flask import Flask, render_template, request, current_app, redirect, url_for, session
from flask import Blueprint, render_template, send_from_directory
from db import mysql

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

def cart_info(item): 
    cart_item = {
        'name': item[0],
        'price': item[1],
        'count':item[2],
        'discount': item[3], 
        'id' : item[4]
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
    cur.execute("SELECT p.name, i.price, c.count, i.discount, p.productId FROM CartItem c NATURAL JOIN Products p NATURAL JOIN Inventory i WHERE userId = {}".format(user_id))
    cart_items = cur.fetchall()
    cart_items = list(map(cart_info,cart_items))
    return render_template('cart.html', items=cart_items)

@cart_bp.route('/add')
def add_to_cart(): 
    id = request.args.get('id')
    user_id = session['user_id']
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    cur.execute('select count FROM CartItem c WHERE c.productId = %s AND c.userId = %s', (id, user_id))
    # query for count
    #query for either add or update
    count = cur.fetchone()
    if count == None:
        count = 0
    else:
        count = count[0]
    cur.execute('SELECT MAX(itemNumber) FROM CartItem WHERE userId = %s',(user_id,)); 
    itemNum = cur.fetchone()
    if itemNum[0] == None:
        itemNum = 0
    else:
        current_app.logger.info('retrieve itemnum:{}'.format(itemNum))
        itemNum = int(itemNum[0])

    count+=1
    if count==1:
        cur.execute('INSERT INTO CartItem(itemNumber, userId, productId, count) VALUES (%s,%s,%s,%s)',(itemNum+1,user_id,id,count));
    else:
         cur.execute('''UPDATE CartItem
                    SET count = %s 
                    WHERE userId = %s AND productId = %s;''',
                    (count,user_id,id));
    mysql.connection.commit()
    return redirect('/cart')
    
@cart_bp.route('/subtract')
def subtract_from_cart():
    id = request.args.get('id')
    user_id = session['user_id']
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    cur.execute('select count FROM CartItem c WHERE c.productId = %s AND c.userId = %s', (id, user_id))
    count = cur.fetchone()
    if count == None:
        return redirect('/cart')
    else:
        count = count[0]-1
    if count==0:
        cur.execute('''DELETE FROM CartItem
            WHERE productId = %s AND userID = %s;''',
            (id,user_id));
    else:
        cur.execute('''UPDATE CartItem
            SET count = %s 
            WHERE userId = %s AND productId = %s;''',
            (count,user_id,id));
    mysql.connection.commit()
    #query for count
    #query for either update or delete 
    return redirect('/cart')

    
@cart_bp.route('/delete')
def delete_from_cart():
    id = request.args.get('id')
    user_id = session['user_id']
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM CartItem
        WHERE productId = %s AND userID = %s;''',
        (id,user_id));
    mysql.connection.commit()
    #query for count
    #query for either update or delete 
    return redirect('/cart')

BEGIN TRANSACTION
// check if the transaction is valid from inventory

cart_prods = 
SELECT  CartItem.productId
FROM CartItem
WHERE CartItem.userId = this_user_uid
// maybe make bill items here?

for prod in cart_prods:
	BEGIN TRANSACTION
// check if the transaction is valid from inventory
is_in_inv = 
SELECT  Inventory.productId
FROM Inventory
WHERE Inventory.productId = this_product_uid AND Inventory.supply >= 1
if(is_in_inv != null){
	// if the item is in inventory, then deduct one stock from inventory table
UPDATE Inventory 
SET supply = supply - prod.count
WHERE productId = this_product_uid
// add it to the billitems
INSERT BillItems
INSERT INTO BillItems VALUES (billId, 1, is_in_inv.price, is_in_inv.discount, prod.productId)
// also remove it from the cart
DELETE prod
FROM CartItem
SET supply = supply - 1
WHERE productId = this_product_uid
} else {
continue;
}
COMMIT TRANSACTION
