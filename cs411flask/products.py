from flask import Blueprint, render_template
import csv 
#import mysql.connector as sql

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def products():
    with open('products.csv') as f:
        a = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
    products = a
    return render_template('products.html', products=products[:100])