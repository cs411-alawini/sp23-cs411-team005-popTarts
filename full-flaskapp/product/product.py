from flask import Flask, render_template, request, current_app
from flask import Blueprint, render_template, send_from_directory
from db import mysql

product_bp = Blueprint('product', __name__, url_prefix='/product')


def get_game_info():
    # 假设这是从数据库中获取游戏信息的函数，根据 game_id 返回游戏信息
    game_info = {
        'id': 1.0,
        'name': 'Game Name 1',
        'price': '$39.99',
        'rating': 4.0,
        'description': 'This is the game description...',
        'requirements': [
            {'icon': 'fas fa-desktop', 'text': 'Windows 10'},
            {'icon': 'fas fa-microchip', 'text': 'Intel Core i5-4460'},
            {'icon': 'fas fa-memory', 'text': '8 GB RAM'},
            {'icon': 'fas fa-database', 'text': '30 GB available space'},
            {'icon': 'fas fa-video', 'text': 'NVIDIA GeForce GTX 760'},
        ]
    }
    return game_info


@product_bp.route('/')
def index():
    game_info = get_game_info()
    return render_template('single_product.html', game_info=game_info)



