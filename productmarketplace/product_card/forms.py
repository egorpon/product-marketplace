from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,FloatField,TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed


class ProductForm(FlaskForm):

    title = StringField('Title of the product', validators=[DataRequired()])
    price = FloatField('Price of the product', validators=[DataRequired()])
    description = TextAreaField('Description of the product', validators=[DataRequired()])
    product_picture = FileField('Picture of the product', validators=[FileAllowed(['jpg','png'], 'Only image!'), DataRequired()])
    submit = SubmitField('Post')