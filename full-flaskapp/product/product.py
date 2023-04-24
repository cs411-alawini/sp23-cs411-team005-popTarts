from flask import Flask, render_template, request, current_app, redirect, url_for, session
from flask import Blueprint, render_template, send_from_directory
from db import mysql

product_bp = Blueprint('product', __name__, url_prefix='/product')


def get_game_info(info):
    game_info = {
        'id': info[0],
        'name': info[1],
        'requiredAge': info[3],
        'rating': info[2],
        'pcRequirements':info[4],
        'description': info[5],
        'release date':info[7],
        'imageLink':info[6],
    }
    return game_info
def get_price_info(info):
    price_info = {
        'price':info[0],
        'discount':info[1]
    }
    return price_info
def get_review_info(info): 
    review_info = {
        'name': info[0] + info[1],
        'rating': info[2],
        'reviewText': info[3],
        'upvotes': info[4],
        'verifiedPurchase':info[5],
        'uniqueId': info[6], 
        'productId': info[7]
    }
    return review_info

@product_bp.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    id = request.args.get('id')
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    new_upvotes = request.args.get('upvote')
    uniqueId = request.args.get('uniqueId')
    if new_upvotes != None and uniqueId != None: 
        new_upvotes = int(new_upvotes)
        uniqueId = int(uniqueId)
        cur.execute("""UPDATE Reviews
                    SET upvotes = %s
                    WHERE uniqueId = %s
                    """, (new_upvotes, uniqueId))
        mysql.connection.commit()
    cur.execute('SELECT * FROM Products WHERE productId = %s', [id])
    info = cur.fetchone()
    game_info = get_game_info(info)
    cur.execute('select price,discount from Inventory where productId = %s', [id])
    info = cur.fetchone()
    price_info= get_price_info(info)
    cur.execute('select count FROM CartItem c WHERE c.productId = %s AND c.userId = %s', (id, session['user_id']))
    count = cur.fetchone()
    if count == None:
        count = 0
    else:
        count = count[0]
    cur.execute("""SELECT c.firstName, c.lastName, r.rating, r.reviewText, r.upvotes, r.verifiedPurchase, r.uniqueId, r.productId
                FROM Reviews r LEFT JOIN Customers c ON r.customerId = c.customerId
                WHERE r.productId = %s
                ORDER BY r.upvotes DESC 
                LIMIT 10""",[id])
    reviews = cur.fetchall()
    reviews = list(map(get_review_info,reviews))
    return render_template('single_product.html', game_info=game_info,price_info = price_info, count = count, reviews = reviews) #this count is temporary 

@product_bp.route('/add')
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
    return redirect('/product/?id={}'.format(id))
    
@product_bp.route('/subtract')
def subtract_from_cart():
    id = request.args.get('id')
    user_id = session['user_id']
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    cur.execute('select count FROM CartItem c WHERE c.productId = %s AND c.userId = %s', (id, user_id))
    count = cur.fetchone()
    if count == None:
        return redirect('/product/?id={}'.format(id))
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
    return redirect('/product/?id={}'.format(id))