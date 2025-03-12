from flask import render_template,request, Blueprint, redirect, url_for
from flask_login import current_user, login_required
# from productmarketplace.models

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
    return render_template('marketplace.html')