import os
from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required
import stripe
from dotenv import load_dotenv, dotenv_values


# config = dotenv_values('.env')
load_dotenv()
print(config)

app = Flask(__name__)

# STRIPE_PUBLIC_KEY=config.get('STRIPE_PUBLIC_KEY','')
# STRIPE_SECRET_KEY= config.get('STRIPE_SECRET_KEY','')
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')

stripe.api_key = STRIPE_SECRET_KEY




app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = "warning"


from productmarketplace.core.views import core
from productmarketplace.users.views import users
from productmarketplace.product_card.views import product
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(product)
