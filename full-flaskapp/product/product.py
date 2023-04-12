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

@product_bp.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    id = request.args.get('id')
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Products WHERE productId = %s', [id])
    info = cur.fetchone()
    game_info = get_game_info(info)
    cur.execute('select price,discount from Inventory where productId = %s', [id])
    info = cur.fetchone()
    price_info= get_price_info(info)
    
    return render_template('single_product.html', game_info=game_info,price_info = price_info, count = 0) #this count is temporary 

@product_bp.route('/add')
def add_to_cart(): 
    id = request.args.get('id')
    user_id = session['user_id']
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    info = cur.fetchone()
    game_info = get_game_info(info)
    cur.execute('select price,discount from Inventory where productId = %s', [id])
    info = cur.fetchone()
    price_info= get_price_info(info)
    #cur.execute('select COUNT(*) FROM CartItem c WHERE c.productId = %s AND c.userId = %s', (id, user_id))
    #query for count
    #query for either add or update
    count = 0 
    return render_template('single_product.html', game_info=game_info,price_info = price_info, count = 0)
    
@product_bp.route('/subtract')
def subtract_from_cart():
    id = request.args.get('id')
    user_id = session['user_id']
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    info = cur.fetchone()
    game_info = get_game_info(info)
    cur.execute('select price,discount from Inventory where productId = %s', [id])
    info = cur.fetchone()
    price_info= get_price_info(info)
    #query for count
    #query for either update or delete 
    return render_template('single_product.html', game_info=game_info,price_info = price_info, count = 0)