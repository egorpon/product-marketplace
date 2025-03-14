from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from productmarketplace import db,login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,user_id)

class User(db.Model,UserMixin):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(64),nullable = False,default = 'default_img.jpg')
    email = db.Column(db.String(64), nullable = False, unique = True, index = True)
    username = db.Column(db.String(64), nullable = False, unique = True, index = True)
    password_hash = db.Column(db.String(128), nullable = False, unique = True)

    role_id = db.Column(db.Integer,db.ForeignKey('roles.id', ondelete = 'CASCADE'))

    role = db.relationship('Role', backref= 'users')
    products = db.relationship('Product', backref = 'author', lazy = True)


    def __init__(self, role_id , email, username, password):
        self.role_id  =  role_id 
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'Username: {self.username}'
    
    def has_role(self, role):
        print('called has_role', role)
        return role == self.role.name
    

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.String(64), unique = True, nullable = False)

class Product(db.Model):
    
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    profile_image = db.Column(db.String(64),nullable = False,default = 'default_product_img.jpg')
    name = db.Column(db.String(64), nullable = False)    
    price = db.Column(db.Float, nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    description = db.Column(db.Text, nullable = False)


    def __init__(self, user_id, name, price, description):
        self.user_id = user_id
        self.name = name
        self.price = price
        self.description = description

    def __repr__(self):
        return f'Product Name: {self.name} -- Price: {self.price}'
        
        


