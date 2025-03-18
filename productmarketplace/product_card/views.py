from flask import Blueprint, redirect, render_template, url_for, request, abort, flash
from flask_login import current_user, login_required
from productmarketplace.product_card.forms import ProductForm
from productmarketplace.models import Product
from productmarketplace.product_card.picture_product_handler import add_product_picture
from productmarketplace import db
from productmarketplace import STRIPE_PUBLIC_KEY
import stripe, os

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
        flash('Product added successfully!', 'success')
        return redirect(url_for('core.marketplace'))
    
    for field,errors in form.errors.items():
        for error in errors:
            flash(error,'danger')

    return render_template('post_product.html', form = form)

@product.route('/<int:product_id>')
@login_required
def products(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product, public_key=STRIPE_PUBLIC_KEY )


@product.route('/success')
def thankyou():
    return render_template('success.html')

@product.route('/cancel')
def cancel():
    return render_template('cancel.html')

@product.route('/<int:product_id>/create-checkout-session', methods = ['POST'])
def create_checkout_session(product_id):
    product = Product.query.get_or_404(product_id)
    success_url = os.getenv('SUCCESS_URL', 'https://product-marketplace-92d5d080cdc2.herokuapp.com/success')
    cancel_url = os.getenv('CANCEL_URL', 'https://product-marketplace-92d5d080cdc2.herokuapp.com/cancel')
    session = stripe.checkout.Session.create(
    line_items=[{
        'price_data':{
        'currency':'usd',
        'product_data':{
            'name':product.name,
            'images':['https://media1.tenor.com/m/jUhmP8zSw54AAAAd/%D0%B1%D1%83%D0%B4%D0%B0%D0%BD%D0%BE%D0%B2-sigma.gif'],
            'description':f'Purchasing {product.name}',
            'tax_code': 'txcd_99999999'	
            },
        'unit_amount_decimal':product.price*100},
        
        'quantity':1
        
    }],
    mode = 'payment',
    success_url=success_url,
    cancel_url=cancel_url)

    return redirect(session.url, code=303)




@product.route('/<int:product_id>/update', methods = ['GET','POST'])
@login_required
def update(product_id):
    product_card = Product.query.get_or_404(product_id)

    if product_card.author !=current_user:
        abort(403)


    form = ProductForm(is_update = True)
    
    if form.validate_on_submit():
        if form.product_picture.data:
            pic = add_product_picture(form.product_picture.data, product_card.name)
            product_card.profile_image = pic
        
        
        product_card.name = form.title.data
        product_card.price = form.price.data
        product_card.description = form.description.data
        db.session.commit()
        flash('Product Updated Successfully!', 'success')
        return redirect(url_for('product.products', product_id=product_card.id))



    form.title.data = product_card.name
    form.description.data = product_card.description
    form.price.data = product_card.price
    return render_template('post_product.html', form=form)



@product.route('/<int:product_id>/delete', methods = ['GET','POST'])
@login_required
def delete_product(product_id):
    print('function call')
    product_card = Product.query.get_or_404(product_id)
        
    if product_card.author != current_user:
        abort(403)

    db.session.delete(product_card)
    db.session.commit()
    flash('Deleted succesfully!','success')
    return redirect(url_for('core.marketplace'))