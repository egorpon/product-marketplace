from flask_login import login_required, login_user, logout_user, current_user
from flask import render_template,Blueprint,redirect,url_for, request
from productmarketplace import db
from productmarketplace.users.forms import RegisterForm, LoginForm
from productmarketplace.models import User, Role

users = Blueprint('users',__name__)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@users.route('/register', methods = ['GET', 'POST'])
def register():

    form = RegisterForm()

    form.role.choices = [(role.id,role.name) for role in Role.query.all()]

    if form.validate_on_submit():
        role = db.session.get(Role,form.role.data)
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    )
        
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        print('Thanks for registration!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user is not None and user.check_password(form.password.data):

            login_user(user)
    
            next = request.args.get('next')
            if next and next[0] == '/':
                return redirect(next)
            return redirect(url_for('core.index'))
            
    
    return render_template('login.html', form = form)


@users.route('/account')
@login_required
def account():
    return render_template('account.html')
