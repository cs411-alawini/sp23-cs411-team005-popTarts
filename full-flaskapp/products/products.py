from flask import Blueprint, render_template,request,current_app
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
        'rating': info[4]
    }
    return game_info

@products_bp.route('/products', methods=['POST'])
def get_search_term():
    text = request.form['search'].lower().strip()
    page = request.args.get('page', default=1, type=int)
    products_per_page = request.args.get('products_per_page', default=20, type=int)
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Products")
    total_products = cur.fetchone()[0]
    cur.execute("SELECT p.productId, p.name, p.imageLink, i.price, AVG(r.rating) FROM Products p NATURAL JOIN Inventory i NATURAL JOIN Reviews r WHERE name LIKE '%%{}%%' GROUP BY p.productId ORDER BY p.productId LIMIT %s,%s".format(text), (start_index, products_per_page))
    products = cur.fetchall()
    current_app.logger.info(products)
    products = list(map(translate_game_info,products))
    current_app.logger.info(products)
    return render_template('products.html',  products=products, total_products=total_products, 
                           products_per_page=products_per_page, current_page=page)


@products_bp.route('/products')
def products():

    page = request.args.get('page', default=1, type=int)
    products_per_page = request.args.get('products_per_page', default=20, type=int)
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Products")
    total_products = cur.fetchone()[0]
    cur.execute("SELECT p.productId, p.name, p.imageLink, i.price, AVG(r.rating) FROM Products p NATURAL JOIN Inventory i NATURAL JOIN Reviews r GROUP BY p.productId ORDER BY p.productId LIMIT %s,%s", (start_index, products_per_page))
    products = cur.fetchall()
    current_app.logger.info(products)
    products = list(map(translate_game_info,products))
    return render_template('products.html',  products=products, total_products=total_products, 
                           products_per_page=products_per_page, current_page=page)