from flask import Flask, render_template, request, current_app
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


@product_bp.route('/')
def index():
    id = request.args.get('id')
    current_app.logger.info(id)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Products WHERE productId = %s', [id])
    info = cur.fetchone()
    game_info = get_game_info(info)
    return render_template('single_product.html', game_info=game_info)

