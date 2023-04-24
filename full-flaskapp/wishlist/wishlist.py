from flask import Flask, render_template, request, current_app, redirect, url_for, session
from flask import Blueprint, render_template, send_from_directory
from db import mysql

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

def wishlist_info(item): 
    wishlist_item = {
        'name': item[0],
        'price': item[1],
        'discount': item[2],
        'id' : item[3]
    }
    return wishlist_item

@wishlist_bp.route('/')
def wishlist():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    else: 
        user_id = session['user_id']
    # Get the user's wishlist items from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.name, i.price, i.discount, p.productId FROM WishList w NATURAL JOIN Products p NATURAL JOIN Inventory i WHERE userId = {}".format(user_id))
    wishlist_items = cur.fetchall()
    wishlist_items = list(map(wishlist_info,wishlist_items))
    return render_template('wishlist.html', items=wishlist_items)

@wishlist_bp.route('/add')
def add_to_wishlist(): 
    id = request.args.get('id')
    user_id = session['user_id']
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    cur.execute('select * FROM WishList c WHERE c.productId = %s AND c.userId = %s', (id, user_id))
    exists = cur.fetchone()
    if exists == None:
        cur.execute('SELECT MAX(itemNumber) FROM WishList WHERE userId = %s',(user_id,)); 
        itemNum = cur.fetchone()
        if itemNum[0] == None:
            itemNum = 0
        else:
            current_app.logger.info('retrieve itemnum:{}'.format(itemNum))
            itemNum = int(itemNum[0])
        cur.execute('INSERT INTO WishList(itemNumber, userId, productId) VALUES (%s,%s,%s)',(itemNum+1,user_id,id));
        mysql.connection.commit()
    return redirect('/wishlist')

@wishlist_bp.route('/delete')
def delete_from_cart():
    id = request.args.get('id')
    user_id = session['user_id']
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM WishList
        WHERE productId = %s AND userID = %s;''',
        (id,user_id));
    mysql.connection.commit()
    #query for count
    #query for either update or delete 
    return redirect('/wishlist')

@wishlist_bp.route('/cartadd')
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
    return redirect('/wishlist/delete?id={}'.format(id))