from flask import Blueprint, render_template, send_from_directory

bp = Blueprint('site', __name__, url_prefix='/site')


@bp.route('/')
def index():
    return render_template('single_product.html')
