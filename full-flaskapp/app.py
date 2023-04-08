# app.py

from flask import Flask, render_template, redirect, url_for, request
from db import mysql

app = Flask(__name__)
app.config['MYSQL_HOST'] = '34.173.32.130'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'poptarts'
app.config['MYSQL_DB'] = 'cs411'
app.secret_key = 'popTarts'

from auth.login import login_blueprint
from auth.logout import logout_blueprint
from auth.register import register_blueprint
from auth.home import home_blueprint
from products.products import products_bp
from product.product import product_bp

app.register_blueprint(login_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(products_bp)
app.register_blueprint(product_bp)

mysql.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

