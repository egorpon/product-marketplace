from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField,FloatField,TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed


class ProductForm(FlaskForm):

    title = StringField('Title of the product', validators=[DataRequired(),Length(min=2, max=20)])
    price = FloatField('Price of the product', validators=[DataRequired('Price must contain numbers')])
    description = TextAreaField('Description of the product', validators=[DataRequired(),Length(min=2, max=5000)])
    product_picture = FileField('Picture of the product', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Post')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if kwargs.get('is_update',False):
            self.product_picture.validators = [FileAllowed(['jpg', 'png'])]
        else:
            self.product_picture.validators = [DataRequired(), FileAllowed(['jpg', 'png'],message='Image must be jpg or png format')]