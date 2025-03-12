from flask_wtf import FlaskForm
from wtforms.validators import EqualTo, Email, DataRequired
from wtforms import StringField,PasswordField,EmailField,SubmitField,ValidationError, SelectField
from flask_wtf.file import FileField, FileAllowed
from productmarketplace.models import User


class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:' ,validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    username = StringField('Username:', validators=[DataRequired()])
    role = SelectField('Who are you?:',coerce=int, choices=[], validators= [DataRequired()])
    password = PasswordField('Password:' ,validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords doesnt match')])
    pass_confirm = PasswordField('Confirm Passowrd:', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,email):
        if User.query.filter_by(email = email.data).first():
            ValidationError('Email has been registered!')
    
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            ValidationError('Username has been registered!')
