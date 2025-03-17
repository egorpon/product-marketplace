from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template,Blueprint,redirect,url_for, request, flash
from productmarketplace import db
from productmarketplace.users.forms import RegisterForm, LoginForm, UpdateUserForm
from productmarketplace.models import User, Role, Product
from productmarketplace.users.picture_handler import add_profile_picture

users = Blueprint('users',__name__)

@users.route('/logout')
@login_required
def logout():
    flash('You have been logged out', 'warning')
    logout_user()
    return redirect(url_for('core.index'))

@users.route('/register', methods = ['GET', 'POST'])
def register():

    form = RegisterForm()

    form.role.choices = [(role.id,role.name) for role in Role.query.all()]

    if form.validate_on_submit():
        existing_email = User.query.filter_by(email = form.email.data).first()
        existing_username = User.query.filter_by(username = form.username.data).first()
        if existing_email:
            flash('Email has been registered!','danger')
        
        elif existing_username:
            flash('Username has been registered!','danger')
        else:    
            role = db.session.get(Role,form.role.data)
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        role_id= role.id
                        )
            
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registration!','success')
            return redirect(url_for('users.login'))
    for field,errors in form.errors.items():
        for error in errors:
            flash(error,'danger')
    return render_template('register.html', form=form)

@users.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user is None:
            flash('Invalid email','danger')
        
        elif not user.check_password(form.password.data):
            flash('Invalid password','danger')
        
        else:
                login_user(user)

                next = request.args.get('next')
                if next and next[0] == '/':
                    return redirect(next)
                flash('Welcome! :)','success')
                return redirect(url_for('core.index'))
    return render_template('login.html', form = form)


@users.route('/account', methods = ['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    form.role.choices = [(role.id,role.name) for role in Role.query.all()]

    if form.validate_on_submit():
        if form.account_picture.data:
            username = current_user.username
            picture = add_profile_picture(form.account_picture.data, username)
            current_user.profile_image = picture

        current_user.username = form.username.data
        current_user.email =  form.email.data

        role = db.session.get(Role,form.role.data)
        current_user.role_id = role.id
        
        db.session.commit()
        flash('User Account Updated!', 'success')
        return redirect(url_for('users.account'))
    
    form.email.data = current_user.email
    form.username.data = current_user.username
    form.role.data = current_user.role_id


    profile_img = url_for('static', filename = 'profile_picture/' + current_user.profile_image )

    for field,errors in form.errors.items():
        for error in errors:
            flash(error,'danger')

    return render_template('account.html', form=form, profile_img = profile_img)


@users.route('/<username>', methods = ['GET','POST'])
@login_required
def user_products(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    product_cards = Product.query.filter_by(author= user).order_by(Product.date.desc()).paginate(page=page,per_page=8)
    return render_template('user_products.html', product_cards=product_cards,user = user)