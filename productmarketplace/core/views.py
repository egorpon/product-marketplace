from flask import render_template,request, Blueprint, redirect, url_for, request
from flask_login import current_user, login_required
from productmarketplace.models import Product

core = Blueprint('core', __name__)

@core.route('/')
def index():
    return render_template('index.html')

@core.route('/info')
def info_page():
    return render_template('info_page.html')

@core.route('/marketplace')
@login_required
def marketplace():
    page = request.args.get('page',1,type=int)
    product_cards = Product.query.order_by(Product.date.asc()).paginate(page=page, per_page=8)
    return render_template('marketplace.html', product_cards = product_cards)