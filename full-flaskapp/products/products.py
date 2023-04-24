from flask import Blueprint, render_template,request,current_app, redirect, url_for, session
import csv 
from db import mysql


products_bp = Blueprint('products', __name__)

def translate_game_info(info):
    print(info)
    game_info = {
        'id': info[0],
        'name': info[1],
        'imageLink':info[2],
        'price': info[3],
        'rating': info[4],
        'discount': info[5]
    }
    return game_info

@products_bp.route('/products', methods=['GET'])
def get_search_term():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    # text = request.form['search'].lower().strip()
    genre = request.args.get('search_genre', default='', type=str)
    text = request.args.get('search', default='', type=str)
    page = request.args.get('page', default=1, type=int)
    current_app.logger.info('search text : '+text)
    products_per_page = request.args.get('products_per_page', default=20, type=int)
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Products")
    total_products = cur.fetchone()[0]
    if text == '' and genre != '': 
        cur.execute("""SELECT p.productId, p.name, p.imageLink, i.price, AVG(r.rating), i.discount
                    FROM Products p LEFT JOIN Inventory i ON p.productId = i.productId 
                    LEFT JOIN Reviews r ON p.productId = r.productId LEFT JOIN GameType g on p.productId = g.productId
                    WHERE g.genre = %s
                    GROUP BY p.productId ORDER BY AVG(r.rating) DESC , p.productId LIMIT %s,%s
                    """, (genre, start_index, products_per_page))
        products = cur.fetchall()
        products = list(map(translate_game_info, products))
        return render_template('products.html',  products=products, total_products=total_products, 
                           products_per_page=products_per_page, current_page=page,search_genre=text)
    else: 
        cur.execute("""SELECT p.productId, p.name, p.imageLink, i.price, AVG(r.rating), i.discount
                    FROM Products p LEFT JOIN Inventory i ON p.productId = i.productId 
                    LEFT JOIN Reviews r ON p.productId = r.productId WHERE name LIKE '%%{}%%' 
                    GROUP BY p.productId ORDER BY p.productId LIMIT %s,%s""".format(text), (start_index, products_per_page))
        #cur.execute("""SELECT p.productId, p.name, p.imageLink, i.price, AVG(r.rating) 
                    # FROM Products p NATURAL JOIN Inventory i NATURAL JOIN Reviews r 
                    # WHERE name LIKE '%%{}%%' GROUP BY p.productId ORDER BY p.productId 
                    # LIMIT %s,%s""".format(text), (start_index, products_per_page))

        products = cur.fetchall()
        products = list(map(translate_game_info,products))
        return render_template('products.html',  products=products, total_products=total_products, 
                            products_per_page=products_per_page, current_page=page,search=text)

@products_bp.route('/products/filtered', methods=['GET'])
def get_filtered(): 
    if 'username' not in session:
        return redirect(url_for('login.login'))
    page = request.args.get('page', default=1, type=int)
    products_per_page = request.args.get('products_per_page', default=20, type=int)
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Products")
    total_products = cur.fetchone()[0]
    cur.execute("SELECT p.productId, p.name, p.imageLink, i.price, AVG(r.rating), i.discount FROM Products p NATURAL JOIN Inventory i NATURAL JOIN Reviews r WHERE i.price <= (SELECT AVG(price) FROM Inventory i) GROUP BY p.productId ORDER BY p.productId LIMIT %s,%s", (start_index, products_per_page))
    products = cur.fetchall()
    # current_app.logger.info(products)
    products = list(map(translate_game_info,products))
    return render_template('products.html',  products=products, total_products=total_products, 
                           products_per_page=products_per_page, current_page=page)

@products_bp.route('/products/high-rating', methods=['GET'])
def get_high_rated(): 
    if 'username' not in session:
        return redirect(url_for('login.login'))
    page = request.args.get('page', default=1, type=int)
    products_per_page = request.args.get('products_per_page', default=20, type=int)
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Products")
    total_products = cur.fetchone()[0]
    cur.execute("""SELECT p.productId, p.name, p.imageLink, i.price, AVG(r.rating) AS Average_Rating, i.discount FROM Products p NATURAL JOIN Inventory i JOIN Reviews r 
ON (p.productId = r.productId)
WHERE i.supply > 0
GROUP BY p.productId
HAVING AVG(r.rating) > 4
ORDER BY p.productId
LIMIT %s,%s""", (start_index, products_per_page))
    products = cur.fetchall()
    # current_app.logger.info(products)
    products = list(map(translate_game_info,products))
    return render_template('products.html',  products=products, total_products=total_products, 
                           products_per_page=products_per_page, current_page=page)
    
