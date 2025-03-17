from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField,FloatField,TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed


class ProductForm(FlaskForm):

    title = StringField('Title of the product', validators=[DataRequired(),Length(min=2, max=20)])
    price = FloatField('Price of the product', validators=[DataRequired('Price must contain numbers')])
    description = TextAreaField('Description of the product', validators=[DataRequired(),Length(min=2, max=5000)])
    product_picture = FileField('Picture of the product', validators=[FileAllowed(['jpg','png'], 'Image must be jpg or png format'), DataRequired()])
    submit = SubmitField('Post')