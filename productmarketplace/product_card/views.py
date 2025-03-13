from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from productmarketplace.product_card.forms import ProductForm
from productmarketplace.models import Product
from productmarketplace.product_card.picture_product_handler import add_product_picture
from productmarketplace import db

product = Blueprint('product', __name__)


@product.route('/post_product', methods = ['GET', 'POST'])
@login_required
def post_product():
    form = ProductForm()
    
    if form.validate_on_submit():
        product = Product(user_id=current_user.id,
                          name = form.title.data,
                          price = form.price.data,
                          description= form.description.data)
        if form.product_picture.data:
            picture_product = add_product_picture(form.product_picture.data, product.name)
            product.profile_image = picture_product
        
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('core.marketplace'))
    
    return render_template('post_product.html', form = form)


# @product.route('/')