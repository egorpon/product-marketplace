from PIL import Image
from flask import current_app
import os

def add_profile_picture(pic_upload, username):

    filename = pic_upload.filename
    ext_name = filename.split('.')[-1]
    new_file_name = str(username)+'.'+ ext_name

    img_path = os.path.join(current_app.root_path, 'static/profile_picture', new_file_name)

    img_size = (200,200)
    image = Image.open(pic_upload)
    image.thumbnail(img_size)
    image.save(img_path)

    return new_file_name