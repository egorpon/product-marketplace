from flask_wtf import FlaskForm
from wtforms.validators import EqualTo, Email, DataRequired
from wtforms import StringField,PasswordField,EmailField,SubmitField,ValidationError, SelectField
from flask_wtf.file import FileField, FileAllowed
from productmarketplace.models import User
from flask_login import current_user
from flask import flash


class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:' ,validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    username = StringField('Username:', validators=[DataRequired()])
    role = SelectField('Who are you?',coerce=int, choices=[], validators= [DataRequired()])
    password = PasswordField('Password:' ,validators=[DataRequired(), EqualTo('pass_confirm', message="Passwords doesn't match")])
    pass_confirm = PasswordField('Confirm Passowrd:', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,email):
        if User.query.filter_by(email = email.data).first():
            ValidationError('Email has been registered!')
    
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():            
            ValidationError('Username has been registered!')

class UpdateUserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    role = SelectField('Change Role', choices=[], coerce=int)
    account_picture = FileField('Upload image', validators=[FileAllowed(['jpg','png'],'Image must be png or jpg')])
    submit = SubmitField('Confirm')
    
    def validate_update_email(self,email):
        if current_user.email != email.data:
            if User.query.filter_by(email=email.data).first():
                flash('Email has been registered!')
                ValidationError('Email has been registered!')

    def validate_update_username(self,username):
        if current_user.username != username.data:
            if User.query.filter_by(username=username.data).first():
                flash('Username has been registered!')
                ValidationError('Username has been registered!')