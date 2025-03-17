from PIL import Image
from flask import current_app
import os

def add_product_picture(pic_upload, name):

    filename = pic_upload.filename
    ext_name = filename.split('.')[-1]
    new_file_name = str(name)+'.'+ ext_name

    img_path = os.path.join(current_app.root_path, 'static/product_picture', new_file_name)

    img_size = (200,200)
    image = Image.open(pic_upload)
    image.thumbnail(img_size)
    image.save(img_path)

    return new_file_name